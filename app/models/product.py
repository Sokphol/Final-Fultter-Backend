from datetime import datetime
from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    short_description = db.Column(db.String(500), nullable=True)
    sku = db.Column(db.String(100), unique=True, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    sale_price = db.Column(db.Numeric(10, 2), nullable=True)
    stock_quantity = db.Column(db.Integer, default=0)
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    weight = db.Column(db.Numeric(8, 2), nullable=True)  # in grams
    connectivity = db.Column(db.String(100), nullable=True)  # Bluetooth, Wired, etc.
    driver_size = db.Column(db.String(50), nullable=True)    # e.g. 40mm
    frequency_response = db.Column(db.String(100), nullable=True)  # e.g. 20Hz-20kHz
    impedance = db.Column(db.String(50), nullable=True)      # e.g. 32 Ohm
    battery_life = db.Column(db.String(50), nullable=True)   # e.g. 30 hours
    noise_cancellation = db.Column(db.Boolean, default=False)
    microphone = db.Column(db.Boolean, default=False)
    average_rating = db.Column(db.Numeric(3, 2), default=0.0)
    review_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    sold_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    brand = db.relationship("Brand", back_populates="products")
    category = db.relationship("Category", back_populates="products")
    images = db.relationship("ProductImage", back_populates="product", cascade="all, delete-orphan", order_by="ProductImage.sort_order")
    variants = db.relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="product", cascade="all, delete-orphan")
    cart_items = db.relationship("CartItem", back_populates="product")
    order_items = db.relationship("OrderItem", back_populates="product")
    wishlist_items = db.relationship("Wishlist", back_populates="product", cascade="all, delete-orphan")

    @property
    def effective_price(self):
        return float(self.sale_price) if self.sale_price else float(self.price)

    @property
    def primary_image(self):
        for img in self.images:
            if img.is_primary:
                return img.image_url
        return self.images[0].image_url if self.images else None

    @property
    def discount_percentage(self):
        if self.sale_price and self.price > 0:
            return round((1 - float(self.sale_price) / float(self.price)) * 100)
        return 0

    def to_dict(self, full=False):
        data = {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "short_description": self.short_description,
            "price": float(self.price),
            "sale_price": float(self.sale_price) if self.sale_price else None,
            "effective_price": self.effective_price,
            "discount_percentage": self.discount_percentage,
            "stock_quantity": self.stock_quantity,
            "is_active": self.is_active,
            "is_featured": self.is_featured,
            "is_in_stock": self.stock_quantity > 0,
            "average_rating": float(self.average_rating),
            "review_count": self.review_count,
            "sold_count": self.sold_count,
            "primary_image": self.primary_image,
            "images": [img.to_dict() for img in self.images],
            "brand": self.brand.to_dict() if self.brand else None,
            "category": self.category.to_dict() if self.category else None,
            "variants": [v.to_dict() for v in self.variants],
            "created_at": self.created_at.isoformat(),
        }
        if full:
            data.update({
                "description": self.description,
                "sku": self.sku,
                "weight": float(self.weight) if self.weight else None,
                "connectivity": self.connectivity,
                "driver_size": self.driver_size,
                "frequency_response": self.frequency_response,
                "impedance": self.impedance,
                "battery_life": self.battery_life,
                "noise_cancellation": self.noise_cancellation,
                "microphone": self.microphone,
                "view_count": self.view_count,
                "updated_at": self.updated_at.isoformat(),
            })
        return data

    def __repr__(self):
        return f"<Product {self.name}>"


class ProductImage(db.Model):
    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    alt_text = db.Column(db.String(200), nullable=True)
    is_primary = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship("Product", back_populates="images")

    def to_dict(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "alt_text": self.alt_text,
            "is_primary": self.is_primary,
            "sort_order": self.sort_order,
        }


class ProductVariant(db.Model):
    __tablename__ = "product_variants"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    color_name = db.Column(db.String(50), nullable=False)
    color_hex = db.Column(db.String(10), nullable=True)   # e.g. #FF5733
    image_url = db.Column(db.String(500), nullable=True)
    stock_quantity = db.Column(db.Integer, default=0)
    price_adjustment = db.Column(db.Numeric(10, 2), default=0.00)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship("Product", back_populates="variants")
    cart_items = db.relationship("CartItem", back_populates="variant")
    order_items = db.relationship("OrderItem", back_populates="variant")

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "color_name": self.color_name,
            "color_hex": self.color_hex,
            "image_url": self.image_url,
            "stock_quantity": self.stock_quantity,
            "price_adjustment": float(self.price_adjustment),
            "is_active": self.is_active,
        }
