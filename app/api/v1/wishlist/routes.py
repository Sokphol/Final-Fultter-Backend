from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.wishlist_service import WishlistService
from app.utils.response import success_response, error_response, paginated_response
from app.utils.pagination import get_pagination_params

wishlist_bp = Blueprint("wishlist", __name__)


@wishlist_bp.route("/", methods=["GET"])
@jwt_required()
def get_wishlist():
    """GET /api/v1/wishlist/"""
    page, per_page = get_pagination_params()
    items, total = WishlistService.get_wishlist(get_jwt_identity(), page, per_page)
    return paginated_response(items, total, page, per_page, "Wishlist fetched")


@wishlist_bp.route("/<int:product_id>", methods=["POST"])
@jwt_required()
def add_to_wishlist(product_id):
    """POST /api/v1/wishlist/<product_id>"""
    result, err = WishlistService.add(get_jwt_identity(), product_id)
    if err:
        return error_response(err, 400)
    return success_response(result, "Added to wishlist", 201)


@wishlist_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def remove_from_wishlist(product_id):
    """DELETE /api/v1/wishlist/<product_id>"""
    _, err = WishlistService.remove(get_jwt_identity(), product_id)
    if err:
        return error_response(err, 404)
    return success_response({}, "Removed from wishlist")


@wishlist_bp.route("/<int:product_id>/check", methods=["GET"])
@jwt_required()
def check_wishlist(product_id):
    """GET /api/v1/wishlist/<product_id>/check"""
    result, _ = WishlistService.check(get_jwt_identity(), product_id)
    return success_response(result, "Wishlist status checked")


@wishlist_bp.route("/clear", methods=["DELETE"])
@jwt_required()
def clear_wishlist():
    """DELETE /api/v1/wishlist/clear"""
    WishlistService.clear(get_jwt_identity())
    return success_response({}, "Wishlist cleared")
