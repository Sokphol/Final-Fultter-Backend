from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.payment_service import PaymentService
from app.utils.response import success_response, error_response
from app.utils.decorators import admin_required

payments_bp = Blueprint("payments", __name__)


@payments_bp.route("/order/<int:order_id>", methods=["GET"])
@jwt_required()
def get_payment_by_order(order_id):
    """GET /api/v1/payments/order/<order_id>"""
    result, err = PaymentService.get_by_order(order_id, get_jwt_identity())
    if err:
        return error_response(err, 404)
    return success_response(result, "Payment fetched")


@payments_bp.route("/order/<int:order_id>/confirm", methods=["PATCH"])
@admin_required
def confirm_payment(order_id):
    """PATCH /api/v1/payments/order/<id>/confirm — Admin."""
    data = request.get_json() or {}
    result, err = PaymentService.confirm_payment(order_id, data.get("transaction_id"))
    if err:
        return error_response(err, 400)
    return success_response(result, "Payment confirmed")


@payments_bp.route("/order/<int:order_id>/refund", methods=["PATCH"])
@admin_required
def refund_payment(order_id):
    """PATCH /api/v1/payments/order/<id>/refund — Admin."""
    result, err = PaymentService.refund_payment(order_id)
    if err:
        return error_response(err, 400)
    return success_response(result, "Payment refunded")
