from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.utils.response import success_response, error_response
from app.utils.decorators import admin_required

users_bp = Blueprint("users", __name__)


@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_my_profile():
    """GET /api/v1/users/me"""
    result, err = UserService.get_by_id(get_jwt_identity())
    if err:
        return error_response(err, 404)
    return success_response(result, "Profile fetched")


@users_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_my_profile():
    """PUT /api/v1/users/me"""
    data = request.get_json()
    result, err = UserService.update(get_jwt_identity(), data or {})
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Profile updated")
