from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.cart_service import CartService
from app.utils.response import success_response, error_response

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/", methods=["GET"])
@jwt_required()
def get_cart():
    """GET /api/v1/cart/"""
    result, err = CartService.get_cart(get_jwt_identity())
    if err:
        return error_response(err, 400)
    return success_response(result, "Cart fetched")


@cart_bp.route("/items", methods=["POST"])
@jwt_required()
def add_to_cart():
    """POST /api/v1/cart/items — Add item to cart."""
    data = request.get_json()
    if not data:
        return error_response("No data provided", 400)
    result, err = CartService.add_item(get_jwt_identity(), data)
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Item added to cart")


@cart_bp.route("/items/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_cart_item(item_id):
    """PUT /api/v1/cart/items/<id> — Update item quantity."""
    data = request.get_json()
    if not data:
        return error_response("No data provided", 400)
    result, err = CartService.update_item(get_jwt_identity(), item_id, data)
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Cart item updated")


@cart_bp.route("/items/<int:item_id>", methods=["DELETE"])
@jwt_required()
def remove_cart_item(item_id):
    """DELETE /api/v1/cart/items/<id>"""
    result, err = CartService.remove_item(get_jwt_identity(), item_id)
    if err:
        return error_response(err, 404)
    return success_response(result, "Item removed from cart")


@cart_bp.route("/clear", methods=["DELETE"])
@jwt_required()
def clear_cart():
    """DELETE /api/v1/cart/clear"""
    result, err = CartService.clear_cart(get_jwt_identity())
    if err:
        return error_response(err, 400)
    return success_response(result, "Cart cleared")
