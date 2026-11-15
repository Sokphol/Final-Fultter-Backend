from app.models.user import User
from app.extensions import db
from app.schemas.user_schema import UserUpdateSchema
from marshmallow import ValidationError


class UserService:

    @staticmethod
    def get_all(page: int = 1, per_page: int = 20, search: str = None):
        query = User.query
        if search:
            query = query.filter(
                db.or_(
                    User.name.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                )
            )
        query = query.order_by(User.created_at.desc())
        from app.utils.pagination import paginate_query
        items, total = paginate_query(query, page, per_page)
        return [u.to_dict() for u in items], total

    @staticmethod
    def get_by_id(user_id: int):
        user = User.query.get(user_id)
        if not user:
            return None, "User not found"
        return user.to_dict(), None

    @staticmethod
    def update(user_id: int, data: dict):
        user = User.query.get(user_id)
        if not user:
            return None, "User not found"
        schema = UserUpdateSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages
        for key, value in validated.items():
            setattr(user, key, value)
        db.session.commit()
        return user.to_dict(), None

    @staticmethod
    def toggle_active(user_id: int):
        user = User.query.get(user_id)
        if not user:
            return None, "User not found"
        user.is_active = not user.is_active
        db.session.commit()
        return user.to_dict(), None

    @staticmethod
    def set_role(user_id: int, role: str):
        if role not in ("customer", "admin"):
            return None, "Invalid role"
        user = User.query.get(user_id)
        if not user:
            return None, "User not found"
        user.role = role
        db.session.commit()
        return user.to_dict(), None
