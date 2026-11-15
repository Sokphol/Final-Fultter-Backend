from app.models.category import Category
from app.extensions import db
from app.schemas.category_schema import CategoryCreateSchema, CategoryUpdateSchema
from app.utils.slugify import unique_slug
from marshmallow import ValidationError


class CategoryService:

    @staticmethod
    def get_all(active_only: bool = False):
        query = Category.query
        if active_only:
            query = query.filter_by(is_active=True)
        categories = query.order_by(Category.sort_order.asc(), Category.name.asc()).all()
        return [c.to_dict() for c in categories], None

    @staticmethod
    def get_by_id(category_id: int):
        cat = Category.query.get(category_id)
        if not cat:
            return None, "Category not found"
        return cat.to_dict(), None

    @staticmethod
    def get_by_slug(slug: str):
        cat = Category.query.filter_by(slug=slug).first()
        if not cat:
            return None, "Category not found"
        return cat.to_dict(), None

    @staticmethod
    def create(data: dict):
        schema = CategoryCreateSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages

        slug = unique_slug(validated["name"], Category)
        cat = Category(slug=slug, **validated)
        db.session.add(cat)
        db.session.commit()
        return cat.to_dict(), None

    @staticmethod
    def update(category_id: int, data: dict):
        cat = Category.query.get(category_id)
        if not cat:
            return None, "Category not found"
        schema = CategoryUpdateSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages
        if "name" in validated:
            validated["slug"] = unique_slug(validated["name"], Category, instance_id=category_id)
        for key, value in validated.items():
            setattr(cat, key, value)
        db.session.commit()
        return cat.to_dict(), None

    @staticmethod
    def delete(category_id: int):
        cat = Category.query.get(category_id)
        if not cat:
            return None, "Category not found"
        if cat.products:
            return None, "Cannot delete category with existing products"
        db.session.delete(cat)
        db.session.commit()
        return True, None
