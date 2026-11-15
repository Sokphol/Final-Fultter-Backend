from app.models.address import Address
from app.extensions import db
from app.schemas.address_schema import AddressCreateSchema, AddressUpdateSchema
from marshmallow import ValidationError


class AddressService:

    @staticmethod
    def get_by_user(user_id: int):
        addresses = Address.query.filter_by(user_id=user_id).order_by(Address.is_default.desc()).all()
        return [a.to_dict() for a in addresses], None

    @staticmethod
    def get_by_id(address_id: int, user_id: int):
        address = Address.query.filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return None, "Address not found"
        return address.to_dict(), None

    @staticmethod
    def create(user_id: int, data: dict):
        schema = AddressCreateSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages

        # If setting as default, unset all others
        if validated.get("is_default"):
            Address.query.filter_by(user_id=user_id, is_default=True).update({"is_default": False})

        # If first address, make it default
        existing = Address.query.filter_by(user_id=user_id).count()
        if existing == 0:
            validated["is_default"] = True

        address = Address(user_id=user_id, **validated)
        db.session.add(address)
        db.session.commit()
        return address.to_dict(), None

    @staticmethod
    def update(address_id: int, user_id: int, data: dict):
        address = Address.query.filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return None, "Address not found"
        schema = AddressUpdateSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages
        if validated.get("is_default"):
            Address.query.filter_by(user_id=user_id, is_default=True).update({"is_default": False})
        for key, value in validated.items():
            setattr(address, key, value)
        db.session.commit()
        return address.to_dict(), None

    @staticmethod
    def delete(address_id: int, user_id: int):
        address = Address.query.filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return None, "Address not found"
        if address.is_default:
            # Try to set another address as default
            other = Address.query.filter(
                Address.user_id == user_id, Address.id != address_id
            ).first()
            if other:
                other.is_default = True
        db.session.delete(address)
        db.session.commit()
        return True, None

    @staticmethod
    def set_default(address_id: int, user_id: int):
        address = Address.query.filter_by(id=address_id, user_id=user_id).first()
        if not address:
            return None, "Address not found"
        Address.query.filter_by(user_id=user_id, is_default=True).update({"is_default": False})
        address.is_default = True
        db.session.commit()
        return address.to_dict(), None
