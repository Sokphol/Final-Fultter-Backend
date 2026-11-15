from app.models.payment import Payment
from app.models.order import Order
from app.extensions import db
from datetime import datetime


class PaymentService:

    @staticmethod
    def get_by_order(order_id: int, user_id: int = None):
        query = Payment.query.filter_by(order_id=order_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        payment = query.first()
        if not payment:
            return None, "Payment not found"
        return payment.to_dict(), None

    @staticmethod
    def confirm_payment(order_id: int, transaction_id: str = None):
        """Admin confirms payment (for bank transfer / manual verification)."""
        payment = Payment.query.filter_by(order_id=order_id).first()
        if not payment:
            return None, "Payment not found"
        if payment.status == Payment.STATUS_PAID:
            return None, "Payment already confirmed"

        payment.status = Payment.STATUS_PAID
        payment.transaction_id = transaction_id
        payment.paid_at = datetime.utcnow()

        order = Order.query.get(order_id)
        if order:
            order.status = Order.STATUS_CONFIRMED

        db.session.commit()
        return payment.to_dict(), None

    @staticmethod
    def refund_payment(order_id: int):
        payment = Payment.query.filter_by(order_id=order_id).first()
        if not payment:
            return None, "Payment not found"
        payment.status = Payment.STATUS_REFUNDED
        db.session.commit()
        return payment.to_dict(), None

    @staticmethod
    def get_all(page: int = 1, per_page: int = 20, status: str = None):
        query = Payment.query
        if status:
            query = query.filter_by(status=status)
        query = query.order_by(Payment.created_at.desc())
        from app.utils.pagination import paginate_query
        items, total = paginate_query(query, page, per_page)
        return [p.to_dict() for p in items], total

