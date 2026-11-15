from flask import Blueprint, request
from app.services.brand_service import BrandService
from app.utils.response import success_response, error_response
from app.utils.decorators import admin_required

brands_bp = Blueprint("brands", __name__)


@brands_bp.route("/", methods=["GET"])
def get_brands():
    """GET /api/v1/brands/ — Public: list all active brands."""
    result, _ = BrandService.get_all(active_only=True)
    return success_response(result, "Brands fetched")


@brands_bp.route("/<int:brand_id>", methods=["GET"])
def get_brand(brand_id):
    """GET /api/v1/brands/<id>"""
    result, err = BrandService.get_by_id(brand_id)
    if err:
        return error_response(err, 404)
    return success_response(result, "Brand fetched")


@brands_bp.route("/slug/<string:slug>", methods=["GET"])
def get_brand_by_slug(slug):
    """GET /api/v1/brands/slug/<slug>"""
    result, err = BrandService.get_by_slug(slug)
    if err:
        return error_response(err, 404)
    return success_response(result, "Brand fetched")


@brands_bp.route("/", methods=["POST"])
@admin_required
def create_brand():
    data = request.get_json()
    result, err = BrandService.create(data or {})
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Brand created", 201)


@brands_bp.route("/<int:brand_id>", methods=["PUT"])
@admin_required
def update_brand(brand_id):
    data = request.get_json()
    result, err = BrandService.update(brand_id, data or {})
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Brand updated")


@brands_bp.route("/<int:brand_id>", methods=["DELETE"])
@admin_required
def delete_brand(brand_id):
    _, err = BrandService.delete(brand_id)
    if err:
        return error_response(err, 400)
    return success_response({}, "Brand deleted")
