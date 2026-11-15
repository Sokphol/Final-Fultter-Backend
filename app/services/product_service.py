from marshmallow import ValidationError
from sqlalchemy.orm import joinedload, selectinload

from app.extensions import db
from app.models.brand import Brand
from app.models.category import Category
from app.models.product import Product, ProductImage, ProductVariant
from app.schemas.product_schema import ProductCreateSchema, ProductUpdateSchema
from app.utils.slugify import unique_slug


class ProductService:

    @staticmethod
    def _with_serialization_relationships(query):
        return query.options(
            joinedload(Product.brand).selectinload(Brand.products),
            joinedload(Product.category).selectinload(Category.products),
            selectinload(Product.images),
            selectinload(Product.variants),
        )

    @staticmethod
    def get_all(page: int = 1, per_page: int = 12, filters: dict = None):
        query = Product.query.filter_by(is_active=True)
        filters = filters or {}

        if filters.get("category_id"):
            query = query.filter_by(category_id=filters["category_id"])
        if filters.get("brand_id"):
            query = query.filter_by(brand_id=filters["brand_id"])
        if filters.get("is_featured"):
            query = query.filter_by(is_featured=True)
        if filters.get("min_price") is not None:
            query = query.filter(Product.price >= filters["min_price"])
        if filters.get("max_price") is not None:
            query = query.filter(Product.price <= filters["max_price"])
        if filters.get("noise_cancellation"):
            query = query.filter_by(noise_cancellation=True)
        if filters.get("microphone"):
            query = query.filter_by(microphone=True)
        if filters.get("connectivity"):
            query = query.filter(Product.connectivity.ilike(f"%{filters['connectivity']}%"))
        if filters.get("search"):
            q = f"%{filters['search']}%"
            query = query.filter(
                db.or_(
                    Product.name.ilike(q),
                    Product.description.ilike(q),
                    Product.short_description.ilike(q),
                )
            )
        if filters.get("in_stock"):
            query = query.filter(Product.stock_quantity > 0)

        # Sorting
        sort = filters.get("sort", "newest")
        if sort == "price_asc":
            query = query.order_by(Product.price.asc())
        elif sort == "price_desc":
            query = query.order_by(Product.price.desc())
        elif sort == "rating":
            query = query.order_by(Product.average_rating.desc())
        elif sort == "popular":
            query = query.order_by(Product.sold_count.desc())
        else:  # newest
            query = query.order_by(Product.created_at.desc())

        query = ProductService._with_serialization_relationships(query)
        from app.utils.pagination import paginate_query
        items, total = paginate_query(query, page, per_page)
        return [p.to_dict() for p in items], total

    @staticmethod
    def get_by_id(product_id: int):
        p = ProductService._with_serialization_relationships(
            Product.query.filter_by(id=product_id)
        ).first()
        if not p or not p.is_active:
            return None, "Product not found"
        p.view_count = (p.view_count or 0) + 1
        db.session.commit()
        return p.to_dict(full=True), None

    @staticmethod
    def get_by_slug(slug: str):
        p = ProductService._with_serialization_relationships(
            Product.query.filter_by(slug=slug, is_active=True)
        ).first()
        if not p:
            return None, "Product not found"
        p.view_count = (p.view_count or 0) + 1
        db.session.commit()
        return p.to_dict(full=True), None

    @staticmethod
    def get_featured(limit: int = 10):
        query = Product.query.filter_by(is_active=True, is_featured=True)\
            .order_by(Product.created_at.desc()).limit(limit)
        products = ProductService._with_serialization_relationships(query).all()
        return [p.to_dict() for p in products], None

    @staticmethod
    def get_related(product_id: int, limit: int = 8):
        product = Product.query.get(product_id)
        if not product:
            return [], None
        query = Product.query.filter(
            Product.id != product_id,
            Product.is_active == True,
            db.or_(
                Product.category_id == product.category_id,
                Product.brand_id == product.brand_id,
            )
        ).limit(limit)
        query = ProductService._with_serialization_relationships(query)
        return [p.to_dict() for p in query.all()], None

    @staticmethod
    def create(data: dict):
        schema = ProductCreateSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages

        variants_data = validated.pop("variants", [])
        slug = unique_slug(validated["name"], Product)
        product = Product(slug=slug, **validated)
        db.session.add(product)
        db.session.flush()

        for v_data in variants_data:
            variant = ProductVariant(product_id=product.id, **v_data)
            db.session.add(variant)

        db.session.commit()
        return product.to_dict(full=True), None

    @staticmethod
    def update(product_id: int, data: dict):
        product = Product.query.get(product_id)
        if not product:
            return None, "Product not found"
        schema = ProductUpdateSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages
        if "name" in validated:
            validated["slug"] = unique_slug(validated["name"], Product, instance_id=product_id)
        for key, value in validated.items():
            setattr(product, key, value)
        db.session.commit()
        return product.to_dict(full=True), None

    @staticmethod
    def delete(product_id: int):
        product = Product.query.get(product_id)
        if not product:
            return None, "Product not found"
        product.is_active = False  # Soft delete
        db.session.commit()
        return True, None

    @staticmethod
    def add_image(product_id: int, image_url: str, is_primary: bool = False, alt_text: str = None):
        product = Product.query.get(product_id)
        if not product:
            return None, "Product not found"
        if is_primary:
            ProductImage.query.filter_by(product_id=product_id, is_primary=True).update({"is_primary": False})
        sort_order = len(product.images)
        img = ProductImage(
            product_id=product_id,
            image_url=image_url,
            is_primary=is_primary or sort_order == 0,
            alt_text=alt_text,
            sort_order=sort_order,
        )
        db.session.add(img)
        db.session.commit()
        return img.to_dict(), None

    @staticmethod
    def delete_image(product_id: int, image_id: int):
        img = ProductImage.query.filter_by(id=image_id, product_id=product_id).first()
        if not img:
            return None, "Image not found"
        db.session.delete(img)
        db.session.commit()
        return True, None

    @staticmethod
    def add_variant(product_id: int, data: dict):
        from app.schemas.product_schema import ProductVariantSchema
        schema = ProductVariantSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages
        product = Product.query.get(product_id)
        if not product:
            return None, "Product not found"
        variant = ProductVariant(product_id=product_id, **validated)
        db.session.add(variant)
        db.session.commit()
        return variant.to_dict(), None

    @staticmethod
    def delete_variant(product_id: int, variant_id: int):
        variant = ProductVariant.query.filter_by(id=variant_id, product_id=product_id).first()
        if not variant:
            return None, "Variant not found"
        db.session.delete(variant)
        db.session.commit()
        return True, None
