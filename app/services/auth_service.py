from app.models.user import User
from app.models.cart import Cart
from app.extensions import db
from app.utils.security import hash_password, verify_password
from app.schemas.user_schema import UserRegisterSchema, UserLoginSchema, ChangePasswordSchema
from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import ValidationError


class AuthService:

    @staticmethod
    def register(data: dict):
        schema = UserRegisterSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages

        if User.query.filter_by(email=validated["email"].lower()).first():
            return None, "Email is already registered"

        user = User(
            name=validated["name"],
            email=validated["email"].lower(),
            password_hash=hash_password(validated["password"]),
            phone=validated.get("phone"),
        )
        db.session.add(user)
        db.session.flush()  # get user.id

        # Create empty cart for new user
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()

        tokens = {
            "access_token": create_access_token(identity=str(user.id)),
            "refresh_token": create_refresh_token(identity=str(user.id)),
            "user": user.to_dict(),
        }
        return tokens, None

    @staticmethod
    def login(data: dict):
        schema = UserLoginSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages

        user = User.query.filter_by(email=validated["email"].lower()).first()
        if not user or not verify_password(validated["password"], user.password_hash):
            return None, "Invalid email or password"
        if not user.is_active:
            return None, "Account has been deactivated. Contact support."

        tokens = {
            "access_token": create_access_token(identity=str(user.id)),
            "refresh_token": create_refresh_token(identity=str(user.id)),
            "user": user.to_dict(),
        }
        return tokens, None

    @staticmethod
    def change_password(user_id: int, data: dict):
        schema = ChangePasswordSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages

        user = User.query.get(user_id)
        if not user:
            return None, "User not found"
        if not verify_password(validated["old_password"], user.password_hash):
            return None, "Current password is incorrect"

        user.password_hash = hash_password(validated["new_password"])
        db.session.commit()
        return {"message": "Password changed successfully"}, None
