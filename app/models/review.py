from datetime import datetime
from app.extensions import db


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    title = db.Column(db.String(200), nullable=True)
    body = db.Column(db.Text, nullable=True)
    is_verified_purchase = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=True)
    helpful_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="reviews")
    product = db.relationship("Product", back_populates="reviews")

    __table_args__ = (
        db.UniqueConstraint("user_id", "product_id", name="unique_user_product_review"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user.to_public_dict() if self.user else None,
            "product_id": self.product_id,
            "rating": self.rating,
            "title": self.title,
            "body": self.body,
            "is_verified_purchase": self.is_verified_purchase,
            "helpful_count": self.helpful_count,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<Review {self.id} rating={self.rating}>"
