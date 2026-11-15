from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.order_service import OrderService
from app.utils.response import success_response, error_response, paginated_response
from app.utils.pagination import get_pagination_params

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/", methods=["GET"])
@jwt_required()
def get_my_orders():
    """GET /api/v1/orders/?status=pending&page=1"""
    page, per_page = get_pagination_params()
    status = request.args.get("status")
    items, total = OrderService.get_user_orders(get_jwt_identity(), page, per_page, status)
    return paginated_response(items, total, page, per_page, "Orders fetched")


@orders_bp.route("/", methods=["POST"])
@jwt_required()
def create_order():
    """POST /api/v1/orders/ — Checkout from cart."""
    data = request.get_json()
    if not data:
        return error_response("No data provided", 400)
    result, err = OrderService.create_order(get_jwt_identity(), data)
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Order placed successfully", 201)


@orders_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id):
    """GET /api/v1/orders/<id>"""
    result, err = OrderService.get_order_by_id(order_id, get_jwt_identity())
    if err:
        return error_response(err, 404)
    return success_response(result, "Order fetched")


@orders_bp.route("/number/<string:order_number>", methods=["GET"])
@jwt_required()
def get_order_by_number(order_number):
    """GET /api/v1/orders/number/<order_number>"""
    result, err = OrderService.get_order_by_number(order_number, get_jwt_identity())
    if err:
        return error_response(err, 404)
    return success_response(result, "Order fetched")


@orders_bp.route("/<int:order_id>/cancel", methods=["PATCH"])
@jwt_required()
def cancel_order(order_id):
    """PATCH /api/v1/orders/<id>/cancel"""
    data = request.get_json()
    if not data:
        return error_response("Please provide a cancellation reason", 400)
    result, err = OrderService.cancel_order(order_id, get_jwt_identity(), data)
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Order cancelled")
