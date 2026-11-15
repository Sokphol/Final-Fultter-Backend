from flask import Blueprint, request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token
)
from app.services.auth_service import AuthService
from app.utils.response import success_response, error_response

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """POST /api/v1/auth/register — Register a new customer."""
    data = request.get_json()
    if not data:
        return error_response("No input data provided", 400)
    result, err = AuthService.register(data)
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Registration successful", 201)


@auth_bp.route("/login", methods=["POST"])
def login():
    """POST /api/v1/auth/login — Login and receive JWT tokens."""
    data = request.get_json()
    if not data:
        return error_response("No input data provided", 400)
    result, err = AuthService.login(data)
    if err:
        return error_response(str(err), 401)
    return success_response(result, "Login successful")


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """POST /api/v1/auth/refresh — Get new access token using refresh token."""
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return success_response({"access_token": access_token}, "Token refreshed")


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    """GET /api/v1/auth/me — Get current logged in user."""
    from app.models.user import User
    user = User.query.get(get_jwt_identity())
    if not user:
        return error_response("User not found", 404)
    return success_response(user.to_dict(), "Profile fetched")


@auth_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():
    """PUT /api/v1/auth/change-password — Change password."""
    data = request.get_json()
    if not data:
        return error_response("No input data provided", 400)
    result, err = AuthService.change_password(get_jwt_identity(), data)
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Password changed successfully")


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """POST /api/v1/auth/logout — Logout (client discards token)."""
    return success_response({}, "Logged out successfully")
