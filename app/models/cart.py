from datetime import datetime
from app.extensions import db


class Cart(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="cart")
    items = db.relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items)

    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.items)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "items": [item.to_dict() for item in self.items],
            "total_items": self.total_items,
            "subtotal": float(self.subtotal),
            "updated_at": self.updated_at.isoformat(),
        }


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey("product_variants.id"), nullable=True)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cart = db.relationship("Cart", back_populates="items")
    product = db.relationship("Product", back_populates="cart_items")
    variant = db.relationship("ProductVariant", back_populates="cart_items")

    @property
    def unit_price(self):
        base = self.product.effective_price
        adj = float(self.variant.price_adjustment) if self.variant else 0
        return base + adj

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def to_dict(self):
        return {
            "id": self.id,
            "product": self.product.to_dict(),
            "variant": self.variant.to_dict() if self.variant else None,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "subtotal": self.subtotal,
            "updated_at": self.updated_at.isoformat(),
        }
