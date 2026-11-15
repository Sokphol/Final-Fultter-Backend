from app.models.wishlist import Wishlist
from app.models.product import Product
from app.extensions import db


class WishlistService:

    @staticmethod
    def get_wishlist(user_id: int, page: int = 1, per_page: int = 12):
        query = Wishlist.query.filter_by(user_id=user_id).order_by(Wishlist.created_at.desc())
        from app.utils.pagination import paginate_query
        items, total = paginate_query(query, page, per_page)
        return [w.to_dict() for w in items], total

    @staticmethod
    def add(user_id: int, product_id: int):
        product = Product.query.filter_by(id=product_id, is_active=True).first()
        if not product:
            return None, "Product not found"
        existing = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing:
            return None, "Product already in wishlist"
        item = Wishlist(user_id=user_id, product_id=product_id)
        db.session.add(item)
        db.session.commit()
        return item.to_dict(), None

    @staticmethod
    def remove(user_id: int, product_id: int):
        item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
        if not item:
            return None, "Product not in wishlist"
        db.session.delete(item)
        db.session.commit()
        return True, None

    @staticmethod
    def check(user_id: int, product_id: int):
        item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
        return {"in_wishlist": item is not None}, None

    @staticmethod
    def clear(user_id: int):
        Wishlist.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return True, None

