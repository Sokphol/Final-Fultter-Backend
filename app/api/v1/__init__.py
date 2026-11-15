from flask import Blueprint

api_v1_bp = Blueprint("api_v1", __name__)

from app.api.v1.auth.routes import auth_bp
from app.api.v1.users.routes import users_bp
from app.api.v1.addresses.routes import addresses_bp
from app.api.v1.categories.routes import categories_bp
from app.api.v1.brands.routes import brands_bp
from app.api.v1.products.routes import products_bp
from app.api.v1.cart.routes import cart_bp
from app.api.v1.orders.routes import orders_bp
from app.api.v1.payments.routes import payments_bp
from app.api.v1.reviews.routes import reviews_bp
from app.api.v1.wishlist.routes import wishlist_bp
from app.api.v1.admin.routes import admin_bp

api_v1_bp.register_blueprint(auth_bp, url_prefix="/auth")
api_v1_bp.register_blueprint(users_bp, url_prefix="/users")
api_v1_bp.register_blueprint(addresses_bp, url_prefix="/addresses")
api_v1_bp.register_blueprint(categories_bp, url_prefix="/categories")
api_v1_bp.register_blueprint(brands_bp, url_prefix="/brands")
api_v1_bp.register_blueprint(products_bp, url_prefix="/products")
api_v1_bp.register_blueprint(cart_bp, url_prefix="/cart")
api_v1_bp.register_blueprint(orders_bp, url_prefix="/orders")
api_v1_bp.register_blueprint(payments_bp, url_prefix="/payments")
api_v1_bp.register_blueprint(reviews_bp, url_prefix="/reviews")
api_v1_bp.register_blueprint(wishlist_bp, url_prefix="/wishlist")
api_v1_bp.register_blueprint(admin_bp, url_prefix="/admin")
