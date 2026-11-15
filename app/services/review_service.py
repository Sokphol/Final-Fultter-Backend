from app.models.review import Review
from app.models.product import Product
from app.extensions import db
from app.schemas.review_schema import ReviewCreateSchema, ReviewUpdateSchema
from marshmallow import ValidationError


class ReviewService:

    @staticmethod
    def get_by_product(product_id: int, page: int = 1, per_page: int = 10, rating: int = None):
        query = Review.query.filter_by(product_id=product_id, is_approved=True)
        if rating:
            query = query.filter_by(rating=rating)
        query = query.order_by(Review.created_at.desc())
        from app.utils.pagination import paginate_query
        items, total = paginate_query(query, page, per_page)
        return [r.to_dict() for r in items], total

    @staticmethod
    def get_summary(product_id: int):
        reviews = Review.query.filter_by(product_id=product_id, is_approved=True).all()
        if not reviews:
            return {"average": 0, "count": 0, "distribution": {i: 0 for i in range(1, 6)}}
        total = sum(r.rating for r in reviews)
        dist = {i: 0 for i in range(1, 6)}
        for r in reviews:
            dist[r.rating] += 1
        return {
            "average": round(total / len(reviews), 2),
            "count": len(reviews),
            "distribution": dist,
        }

    @staticmethod
    def create(user_id: int, data: dict):
        schema = ReviewCreateSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages

        product = Product.query.filter_by(id=validated["product_id"], is_active=True).first()
        if not product:
            return None, "Product not found"

        existing = Review.query.filter_by(user_id=user_id, product_id=validated["product_id"]).first()
        if existing:
            return None, "You have already reviewed this product"

        review = Review(user_id=user_id, **validated)
        db.session.add(review)
        db.session.flush()

        # Recalculate product rating
        ReviewService._update_product_rating(validated["product_id"])
        db.session.commit()
        return review.to_dict(), None

    @staticmethod
    def update(review_id: int, user_id: int, data: dict):
        review = Review.query.filter_by(id=review_id, user_id=user_id).first()
        if not review:
            return None, "Review not found"
        schema = ReviewUpdateSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages
        for key, value in validated.items():
            setattr(review, key, value)
        db.session.flush()
        ReviewService._update_product_rating(review.product_id)
        db.session.commit()
        return review.to_dict(), None

    @staticmethod
    def delete(review_id: int, user_id: int, is_admin: bool = False):
        query = Review.query.filter_by(id=review_id)
        if not is_admin:
            query = query.filter_by(user_id=user_id)
        review = query.first()
        if not review:
            return None, "Review not found"
        product_id = review.product_id
        db.session.delete(review)
        db.session.flush()
        ReviewService._update_product_rating(product_id)
        db.session.commit()
        return True, None

    @staticmethod
    def _update_product_rating(product_id: int):
        reviews = Review.query.filter_by(product_id=product_id, is_approved=True).all()
        product = Product.query.get(product_id)
        if not product:
            return
        if reviews:
            avg = sum(r.rating for r in reviews) / len(reviews)
            product.average_rating = round(avg, 2)
            product.review_count = len(reviews)
        else:
            product.average_rating = 0
            product.review_count = 0

