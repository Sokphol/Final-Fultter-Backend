from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.category_service import CategoryService
from app.utils.response import success_response, error_response
from app.utils.decorators import admin_required

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/", methods=["GET"])
def get_categories():
    """GET /api/v1/categories/ — Public: list all active categories."""
    result, _ = CategoryService.get_all(active_only=True)
    return success_response(result, "Categories fetched")


@categories_bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id):
    """GET /api/v1/categories/<id>"""
    result, err = CategoryService.get_by_id(category_id)
    if err:
        return error_response(err, 404)
    return success_response(result, "Category fetched")


@categories_bp.route("/slug/<string:slug>", methods=["GET"])
def get_category_by_slug(slug):
    """GET /api/v1/categories/slug/<slug>"""
    result, err = CategoryService.get_by_slug(slug)
    if err:
        return error_response(err, 404)
    return success_response(result, "Category fetched")


@categories_bp.route("/", methods=["POST"])
@admin_required
def create_category():
    """POST /api/v1/categories/ — Admin: create category."""
    data = request.get_json()
    result, err = CategoryService.create(data or {})
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Category created", 201)


@categories_bp.route("/<int:category_id>", methods=["PUT"])
@admin_required
def update_category(category_id):
    """PUT /api/v1/categories/<id> — Admin."""
    data = request.get_json()
    result, err = CategoryService.update(category_id, data or {})
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Category updated")


@categories_bp.route("/<int:category_id>", methods=["DELETE"])
@admin_required
def delete_category(category_id):
    """DELETE /api/v1/categories/<id> — Admin."""
    _, err = CategoryService.delete(category_id)
    if err:
        return error_response(err, 400)
    return success_response({}, "Category deleted")
