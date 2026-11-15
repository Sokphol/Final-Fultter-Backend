from flask import Blueprint, request
from app.services.user_service import UserService
from app.services.order_service import OrderService
from app.services.payment_service import PaymentService
from app.services.product_service import ProductService
from app.utils.response import success_response, error_response, paginated_response
from app.utils.decorators import admin_required
from app.utils.pagination import get_pagination_params
from app.extensions import db
from app.models.order import Order
from app.models.product import Product
from app.models.user import User

admin_bp = Blueprint("admin", __name__)


# ─── Dashboard Stats ───────────────────────────────────────────────────────────

@admin_bp.route("/stats", methods=["GET"])
@admin_required
def get_stats():
    """GET /api/v1/admin/stats — Dashboard summary."""
    from app.models.payment import Payment
    total_users = User.query.count()
    total_products = Product.query.filter_by(is_active=True).count()
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status=Order.STATUS_PENDING).count()
    revenue = db.session.query(
        db.func.coalesce(db.func.sum(Payment.amount), 0)
    ).filter_by(status=Payment.STATUS_PAID).scalar()

    return success_response({
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "total_revenue": float(revenue),
    }, "Stats fetched")


# ─── Users ─────────────────────────────────────────────────────────────────────

@admin_bp.route("/users", methods=["GET"])
@admin_required
def admin_get_users():
    """GET /api/v1/admin/users?search=&page=1"""
    page, per_page = get_pagination_params()
    search = request.args.get("search")
    items, total = UserService.get_all(page, per_page, search)
    return paginated_response(items, total, page, per_page, "Users fetched")


@admin_bp.route("/users/<int:user_id>", methods=["GET"])
@admin_required
def admin_get_user(user_id):
    result, err = UserService.get_by_id(user_id)
    if err:
        return error_response(err, 404)
    return success_response(result, "User fetched")


@admin_bp.route("/users/<int:user_id>/toggle-active", methods=["PATCH"])
@admin_required
def admin_toggle_user(user_id):
    """PATCH /api/v1/admin/users/<id>/toggle-active"""
    result, err = UserService.toggle_active(user_id)
    if err:
        return error_response(err, 404)
    return success_response(result, "User status updated")


@admin_bp.route("/users/<int:user_id>/set-role", methods=["PATCH"])
@admin_required
def admin_set_role(user_id):
    """PATCH /api/v1/admin/users/<id>/set-role  Body: {"role": "admin"}"""
    data = request.get_json() or {}
    result, err = UserService.set_role(user_id, data.get("role", ""))
    if err:
        return error_response(err, 400)
    return success_response(result, "User role updated")


# ─── Orders ────────────────────────────────────────────────────────────────────

@admin_bp.route("/orders", methods=["GET"])
@admin_required
def admin_get_orders():
    """GET /api/v1/admin/orders?status=&search=&page=1"""
    page, per_page = get_pagination_params()
    status = request.args.get("status")
    search = request.args.get("search")
    items, total = OrderService.admin_get_all(page, per_page, status, search)
    return paginated_response(items, total, page, per_page, "Orders fetched")


@admin_bp.route("/orders/<int:order_id>", methods=["GET"])
@admin_required
def admin_get_order(order_id):
    result, err = OrderService.get_order_by_id(order_id)
    if err:
        return error_response(err, 404)
    return success_response(result, "Order fetched")


@admin_bp.route("/orders/<int:order_id>/status", methods=["PATCH"])
@admin_required
def admin_update_order_status(order_id):
    """PATCH /api/v1/admin/orders/<id>/status  Body: {"status": "shipped"}"""
    data = request.get_json() or {}
    result, err = OrderService.admin_update_status(order_id, data.get("status", ""))
    if err:
        return error_response(err, 400)
    return success_response(result, "Order status updated")


# ─── Payments ──────────────────────────────────────────────────────────────────

@admin_bp.route("/payments", methods=["GET"])
@admin_required
def admin_get_payments():
    """GET /api/v1/admin/payments?status=&page=1"""
    page, per_page = get_pagination_params()
    status = request.args.get("status")
    items, total = PaymentService.get_all(page, per_page, status)
    return paginated_response(items, total, page, per_page, "Payments fetched")


# ─── Products (admin view includes inactive) ───────────────────────────────────

@admin_bp.route("/products", methods=["GET"])
@admin_required
def admin_get_products():
    """GET /api/v1/admin/products — All products including inactive."""
    page, per_page = get_pagination_params()
    query = Product.query
    search = request.args.get("search")
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    query = query.order_by(Product.created_at.desc())
    from app.utils.pagination import paginate_query
    items, total = paginate_query(query, page, per_page)
    return paginated_response([p.to_dict() for p in items], total, page, per_page, "Products fetched")
