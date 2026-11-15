import json
import uuid
from datetime import datetime
from app.models.order import Order, OrderItem
from app.models.cart import Cart, CartItem
from app.models.address import Address
from app.models.payment import Payment
from app.extensions import db
from app.schemas.order_schema import OrderCreateSchema, OrderCancelSchema
from marshmallow import ValidationError


def generate_order_number() -> str:
    return f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"


class OrderService:

    SHIPPING_FEE = 2.50  # Default shipping fee in USD

    @staticmethod
    def create_order(user_id: int, data: dict):
        schema = OrderCreateSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages

        # Validate address belongs to user
        address = Address.query.filter_by(id=validated["address_id"], user_id=user_id).first()
        if not address:
            return None, "Shipping address not found"

        # Get user's cart
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart or not cart.items:
            return None, "Your cart is empty"

        # Validate stock and build order items
        order_items_data = []
        for cart_item in cart.items:
            product = cart_item.product
            variant = cart_item.variant
            stock = variant.stock_quantity if variant else product.stock_quantity

            if stock < cart_item.quantity:
                return None, f"'{product.name}' has insufficient stock (available: {stock})"

            unit_price = cart_item.unit_price
            total_price = unit_price * cart_item.quantity
            snapshot = {
                "id": product.id,
                "name": product.name,
                "sku": product.sku,
                "primary_image": product.primary_image,
                "brand": product.brand.name if product.brand else None,
                "color": variant.color_name if variant else None,
            }
            order_items_data.append({
                "product_id": product.id,
                "variant_id": variant.id if variant else None,
                "quantity": cart_item.quantity,
                "unit_price": unit_price,
                "total_price": total_price,
                "snapshot": snapshot,
                "product": product,
                "variant": variant,
            })

        subtotal = sum(item["total_price"] for item in order_items_data)
        shipping_fee = OrderService.SHIPPING_FEE
        total = subtotal + shipping_fee

        shipping_addr = {
            "full_name": address.full_name,
            "phone": address.phone,
            "street": address.street,
            "city": address.city,
            "state": address.state,
            "postal_code": address.postal_code,
            "country": address.country,
        }

        order = Order(
            user_id=user_id,
            order_number=generate_order_number(),
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            total=total,
            shipping_address=json.dumps(shipping_addr),
            notes=validated.get("notes"),
        )
        db.session.add(order)
        db.session.flush()

        # Create order items and decrement stock
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data["product_id"],
                variant_id=item_data["variant_id"],
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                total_price=item_data["total_price"],
                product_snapshot=json.dumps(item_data["snapshot"]),
            )
            db.session.add(order_item)

            # Decrement stock
            if item_data["variant"]:
                item_data["variant"].stock_quantity -= item_data["quantity"]
                item_data["product"].sold_count = (item_data["product"].sold_count or 0) + item_data["quantity"]
            else:
                item_data["product"].stock_quantity -= item_data["quantity"]
                item_data["product"].sold_count = (item_data["product"].sold_count or 0) + item_data["quantity"]

        # Create payment record
        payment = Payment(
            order_id=order.id,
            user_id=user_id,
            method=validated["payment_method"],
            amount=total,
            status=Payment.STATUS_PENDING,
        )
        db.session.add(payment)

        # Clear cart
        CartItem.query.filter_by(cart_id=cart.id).delete()

        db.session.commit()
        return order.to_dict(full=True), None

    @staticmethod
    def get_user_orders(user_id: int, page: int = 1, per_page: int = 10, status: str = None):
        query = Order.query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        query = query.order_by(Order.created_at.desc())
        from app.utils.pagination import paginate_query
        items, total = paginate_query(query, page, per_page)
        return [o.to_dict(full=True) for o in items], total

    @staticmethod
    def get_order_by_number(order_number: str, user_id: int):
        order = Order.query.filter_by(order_number=order_number, user_id=user_id).first()
        if not order:
            return None, "Order not found"
        return order.to_dict(full=True), None

    @staticmethod
    def get_order_by_id(order_id: int, user_id: int = None):
        query = Order.query.filter_by(id=order_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        order = query.first()
        if not order:
            return None, "Order not found"
        return order.to_dict(full=True), None

    @staticmethod
    def cancel_order(order_id: int, user_id: int, data: dict):
        schema = OrderCancelSchema()
        try:
            validated = schema.load(data)
        except ValidationError as e:
            return None, e.messages

        order = Order.query.filter_by(id=order_id, user_id=user_id).first()
        if not order:
            return None, "Order not found"
        if order.status not in (Order.STATUS_PENDING, Order.STATUS_CONFIRMED):
            return None, f"Cannot cancel order with status '{order.status}'"

        # Restore stock
        for item in order.items:
            if item.variant:
                item.variant.stock_quantity += item.quantity
                item.product.sold_count = max(0, (item.product.sold_count or 0) - item.quantity)
            else:
                item.product.stock_quantity += item.quantity
                item.product.sold_count = max(0, (item.product.sold_count or 0) - item.quantity)

        order.status = Order.STATUS_CANCELLED
        order.cancelled_reason = validated["reason"]
        if order.payment:
            order.payment.status = Payment.STATUS_REFUNDED

        db.session.commit()
        return order.to_dict(full=True), None

    @staticmethod
    def admin_get_all(page: int = 1, per_page: int = 20, status: str = None, search: str = None):
        query = Order.query
        if status:
            query = query.filter_by(status=status)
        if search:
            query = query.filter(Order.order_number.ilike(f"%{search}%"))
        query = query.order_by(Order.created_at.desc())
        from app.utils.pagination import paginate_query
        items, total = paginate_query(query, page, per_page)
        return [o.to_dict(full=True) for o in items], total

    @staticmethod
    def admin_update_status(order_id: int, status: str):
        if status not in Order.VALID_STATUSES:
            return None, f"Invalid status. Valid: {Order.VALID_STATUSES}"
        order = Order.query.get(order_id)
        if not order:
            return None, "Order not found"
        order.status = status
        if status == Order.STATUS_DELIVERED and order.payment:
            order.payment.status = Payment.STATUS_PAID
            order.payment.paid_at = datetime.utcnow()
        db.session.commit()
        return order.to_dict(full=True), None

