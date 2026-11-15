import os
from flask import Flask
from app.extensions import db, migrate, jwt, cors


def create_app(config_name: str = "development") -> Flask:
    """Application factory."""
    app = Flask(__name__)
    from app.config import config_by_name
    app.config.from_object(config_by_name[config_name])

    # Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Import models so Flask-Migrate detects them
    from app.models import user, address, category, brand, product, cart, order, payment, review, wishlist  # noqa

    # Register blueprints
    from app.api.v1 import api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")

    # Static file serving for uploads
    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        from flask import send_from_directory
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    # Register error handlers
    register_error_handlers(app)

    return app


def register_error_handlers(app: Flask):
    from flask import jsonify

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"success": False, "message": "Bad request", "data": None}), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"success": False, "message": "Unauthorized", "data": None}), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({"success": False, "message": "Forbidden", "data": None}), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Resource not found", "data": None}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"success": False, "message": "Method not allowed", "data": None}), 405

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"success": False, "message": "Internal server error", "data": None}), 500
