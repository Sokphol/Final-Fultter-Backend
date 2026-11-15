from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user import User


def get_current_user_id() -> int:
    """Helper to get current user ID as an integer from JWT."""
    identity = get_jwt_identity()
    if identity is None:
        return None
    try:
        return int(identity)
    except (ValueError, TypeError):
        return identity


def admin_required(fn):
    """Allow only admin users."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_current_user_id()
        user = User.query.get(user_id)
        if not user or user.role != "admin":
            return jsonify({"success": False, "message": "Admin access required", "data": None}), 403
        return fn(*args, **kwargs)
    return wrapper


def active_required(fn):
    """Allow only active (non-banned) users."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_current_user_id()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found", "data": None}), 404
        if not user.is_active:
            return jsonify({"success": False, "message": "Account is deactivated", "data": None}), 403
        return fn(*args, **kwargs)
    return wrapper
