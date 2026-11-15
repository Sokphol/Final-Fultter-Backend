from datetime import datetime
from app.extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    METHOD_CASH = "cash_on_delivery"
    METHOD_CARD = "credit_card"
    METHOD_PAYPAL = "paypal"
    METHOD_BANK = "bank_transfer"

    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"
    STATUS_REFUNDED = "refunded"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    method = db.Column(db.String(50), nullable=False, default=METHOD_CASH)
    status = db.Column(db.String(30), default=STATUS_PENDING)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    currency = db.Column(db.String(10), default="USD")
    transaction_id = db.Column(db.String(200), nullable=True)
    payment_details = db.Column(db.Text, nullable=True)  # JSON: gateway response
    paid_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order = db.relationship("Order", back_populates="payment")
    user = db.relationship("User", back_populates="payments")

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "method": self.method,
            "status": self.status,
            "amount": float(self.amount),
            "currency": self.currency,
            "transaction_id": self.transaction_id,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Payment {self.id} {self.status}>"
