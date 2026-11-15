from datetime import datetime
from app.extensions import db


class Wishlist(db.Model):
    __tablename__ = "wishlists"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="wishlist_items")
    product = db.relationship("Product", back_populates="wishlist_items")

    __table_args__ = (
        db.UniqueConstraint("user_id", "product_id", name="unique_user_product_wishlist"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "product": self.product.to_dict(),
            "created_at": self.created_at.isoformat(),
        }
