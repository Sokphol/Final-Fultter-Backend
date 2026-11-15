from app.models.cart import Cart, CartItem
from app.models.product import Product, ProductVariant
from app.extensions import db
from app.schemas.cart_schema import CartAddItemSchema, CartUpdateItemSchema
from marshmallow import ValidationError


class CartService:

    @staticmethod
    def get_or_create_cart(user_id: int):
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()
        return cart

    @staticmethod
    def get_cart(user_id: int):
        cart = CartService.get_or_create_cart(user_id)
        return cart.to_dict(), None

    @staticmethod
    def add_item(user_id: int, data: dict):
        schema = CartAddItemSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages

        product = Product.query.filter_by(id=validated["product_id"], is_active=True).first()
        if not product:
            return None, "Product not found or unavailable"

        variant = None
        if validated.get("variant_id"):
            variant = ProductVariant.query.filter_by(
                id=validated["variant_id"], product_id=product.id, is_active=True
            ).first()
            if not variant:
                return None, "Product variant not found"

        stock = variant.stock_quantity if variant else product.stock_quantity
        if stock < validated["quantity"]:
            return None, f"Insufficient stock. Available: {stock}"

        cart = CartService.get_or_create_cart(user_id)

        # Check if item already in cart
        existing = CartItem.query.filter_by(
            cart_id=cart.id,
            product_id=product.id,
            variant_id=validated.get("variant_id"),
        ).first()

        if existing:
            new_qty = existing.quantity + validated["quantity"]
            if new_qty > stock:
                return None, f"Cannot add more. Stock limit: {stock}"
            existing.quantity = new_qty
        else:
            item = CartItem(
                cart_id=cart.id,
                product_id=product.id,
                variant_id=validated.get("variant_id"),
                quantity=validated["quantity"],
            )
            db.session.add(item)

        db.session.commit()
        return cart.to_dict(), None

    @staticmethod
    def update_item(user_id: int, item_id: int, data: dict):
        schema = CartUpdateItemSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages

        cart = CartService.get_or_create_cart(user_id)
        item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
        if not item:
            return None, "Cart item not found"

        stock = item.variant.stock_quantity if item.variant else item.product.stock_quantity
        if validated["quantity"] > stock:
            return None, f"Insufficient stock. Available: {stock}"

        item.quantity = validated["quantity"]
        db.session.commit()
        return cart.to_dict(), None

    @staticmethod
    def remove_item(user_id: int, item_id: int):
        cart = CartService.get_or_create_cart(user_id)
        item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
        if not item:
            return None, "Cart item not found"
        db.session.delete(item)
        db.session.commit()
        return cart.to_dict(), None

    @staticmethod
    def clear_cart(user_id: int):
        cart = CartService.get_or_create_cart(user_id)
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()
        return cart.to_dict(), None

