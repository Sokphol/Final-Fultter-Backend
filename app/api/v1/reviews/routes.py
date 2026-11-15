from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.review_service import ReviewService
from app.utils.response import success_response, error_response, paginated_response
from app.utils.pagination import get_pagination_params
from app.utils.decorators import admin_required

reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.route("/product/<int:product_id>", methods=["GET"])
def get_product_reviews(product_id):
    """GET /api/v1/reviews/product/<id>?rating=5"""
    page, per_page = get_pagination_params()
    rating = request.args.get("rating", type=int)
    items, total = ReviewService.get_by_product(product_id, page, per_page, rating)
    return paginated_response(items, total, page, per_page, "Reviews fetched")


@reviews_bp.route("/product/<int:product_id>/summary", methods=["GET"])
def get_product_review_summary(product_id):
    """GET /api/v1/reviews/product/<id>/summary"""
    result = ReviewService.get_summary(product_id)
    return success_response(result, "Review summary fetched")


@reviews_bp.route("/", methods=["POST"])
@jwt_required()
def create_review():
    """POST /api/v1/reviews/ — Submit a review."""
    data = request.get_json()
    if not data:
        return error_response("No data provided", 400)
    result, err = ReviewService.create(get_jwt_identity(), data)
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Review submitted", 201)


@reviews_bp.route("/<int:review_id>", methods=["PUT"])
@jwt_required()
def update_review(review_id):
    """PUT /api/v1/reviews/<id>"""
    data = request.get_json()
    result, err = ReviewService.update(review_id, get_jwt_identity(), data or {})
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Review updated")


@reviews_bp.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(review_id):
    """DELETE /api/v1/reviews/<id>"""
    _, err = ReviewService.delete(review_id, get_jwt_identity())
    if err:
        return error_response(err, 404)
    return success_response({}, "Review deleted")
