from app.models.brand import Brand
from app.extensions import db
from app.schemas.brand_schema import BrandCreateSchema, BrandUpdateSchema
from app.utils.slugify import unique_slug
from marshmallow import ValidationError


class BrandService:

    @staticmethod
    def get_all(active_only: bool = False):
        query = Brand.query
        if active_only:
            query = query.filter_by(is_active=True)
        brands = query.order_by(Brand.name.asc()).all()
        return [b.to_dict() for b in brands], None

    @staticmethod
    def get_by_id(brand_id: int):
        brand = Brand.query.get(brand_id)
        if not brand:
            return None, "Brand not found"
        return brand.to_dict(), None

    @staticmethod
    def get_by_slug(slug: str):
        brand = Brand.query.filter_by(slug=slug).first()
        if not brand:
            return None, "Brand not found"
        return brand.to_dict(), None

    @staticmethod
    def create(data: dict):
        schema = BrandCreateSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages
        slug = unique_slug(validated["name"], Brand)
        brand = Brand(slug=slug, **validated)
        db.session.add(brand)
        db.session.commit()
        return brand.to_dict(), None

    @staticmethod
    def update(brand_id: int, data: dict):
        brand = Brand.query.get(brand_id)
        if not brand:
            return None, "Brand not found"
        schema = BrandUpdateSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages
        if "name" in validated:
            validated["slug"] = unique_slug(validated["name"], Brand, instance_id=brand_id)
        for key, value in validated.items():
            setattr(brand, key, value)
        db.session.commit()
        return brand.to_dict(), None

    @staticmethod
    def delete(brand_id: int):
        brand = Brand.query.get(brand_id)
        if not brand:
            return None, "Brand not found"
        if brand.products:
            return None, "Cannot delete brand with existing products"
        db.session.delete(brand)
        db.session.commit()
        return True, None
