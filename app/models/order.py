import json
from datetime import datetime
from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_PROCESSING = "processing"
    STATUS_SHIPPED = "shipped"
    STATUS_DELIVERED = "delivered"
    STATUS_CANCELLED = "cancelled"
    STATUS_REFUNDED = "refunded"

    VALID_STATUSES = [
        STATUS_PENDING, STATUS_CONFIRMED, STATUS_PROCESSING,
        STATUS_SHIPPED, STATUS_DELIVERED, STATUS_CANCELLED, STATUS_REFUNDED
    ]

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    status = db.Column(db.String(30), default=STATUS_PENDING)
    subtotal = db.Column(db.Numeric(12, 2), nullable=False)
    discount_amount = db.Column(db.Numeric(12, 2), default=0.00)
    shipping_fee = db.Column(db.Numeric(12, 2), default=0.00)
    total = db.Column(db.Numeric(12, 2), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)  # JSON string
    notes = db.Column(db.Text, nullable=True)
    cancelled_reason = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="orders")
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payment = db.relationship("Payment", back_populates="order", uselist=False)

    def get_shipping_address(self):
        try:
            return json.loads(self.shipping_address)
        except Exception:
            return {}

    def to_dict(self, full=False):
        data = {
            "id": self.id,
            "order_number": self.order_number,
            "status": self.status,
            "subtotal": float(self.subtotal),
            "discount_amount": float(self.discount_amount),
            "shipping_fee": float(self.shipping_fee),
            "total": float(self.total),
            "shipping_address": self.get_shipping_address(),
            "notes": self.notes,
            "items_count": len(self.items),
            "payment": self.payment.to_dict() if self.payment else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        if full:
            data["items"] = [item.to_dict() for item in self.items]
            data["cancelled_reason"] = self.cancelled_reason
        return data

    def __repr__(self):
        return f"<Order {self.order_number}>"


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey("product_variants.id"), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    product_snapshot = db.Column(db.Text, nullable=True)  # JSON snapshot at time of order

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", back_populates="order_items")
    variant = db.relationship("ProductVariant", back_populates="order_items")

    def get_snapshot(self):
        try:
            return json.loads(self.product_snapshot)
        except Exception:
            return {}

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_snapshot": self.get_snapshot(),
            "variant": self.variant.to_dict() if self.variant else None,
            "quantity": self.quantity,
            "unit_price": float(self.unit_price),
            "total_price": float(self.total_price),
        }
