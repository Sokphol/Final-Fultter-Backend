from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.product_service import ProductService
from app.utils.response import success_response, error_response, paginated_response
from app.utils.decorators import admin_required
from app.utils.pagination import get_pagination_params
from app.utils.upload import save_file

products_bp = Blueprint("products", __name__)


@products_bp.route("/", methods=["GET"])
def get_products():
    """GET /api/v1/products/?page=1&per_page=12&search=&category_id=&brand_id=&sort=newest"""
    page, per_page = get_pagination_params()
    filters = {
        "search": request.args.get("search"),
        "category_id": request.args.get("category_id", type=int),
        "brand_id": request.args.get("brand_id", type=int),
        "min_price": request.args.get("min_price", type=float),
        "max_price": request.args.get("max_price", type=float),
        "is_featured": request.args.get("is_featured", type=bool),
        "in_stock": request.args.get("in_stock", type=bool),
        "noise_cancellation": request.args.get("noise_cancellation", type=bool),
        "microphone": request.args.get("microphone", type=bool),
        "connectivity": request.args.get("connectivity"),
        "sort": request.args.get("sort", "newest"),
    }
    items, total = ProductService.get_all(page, per_page, filters)
    return paginated_response(items, total, page, per_page, "Products fetched")


@products_bp.route("/featured", methods=["GET"])
def get_featured():
    """GET /api/v1/products/featured"""
    limit = request.args.get("limit", 10, type=int)
    result, _ = ProductService.get_featured(limit)
    return success_response(result, "Featured products fetched")


@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """GET /api/v1/products/<id>"""
    result, err = ProductService.get_by_id(product_id)
    if err:
        return error_response(err, 404)
    return success_response(result, "Product fetched")


@products_bp.route("/slug/<string:slug>", methods=["GET"])
def get_product_by_slug(slug):
    """GET /api/v1/products/slug/<slug>"""
    result, err = ProductService.get_by_slug(slug)
    if err:
        return error_response(err, 404)
    return success_response(result, "Product fetched")


@products_bp.route("/<int:product_id>/related", methods=["GET"])
def get_related(product_id):
    """GET /api/v1/products/<id>/related"""
    limit = request.args.get("limit", 8, type=int)
    result, _ = ProductService.get_related(product_id, limit)
    return success_response(result, "Related products fetched")


@products_bp.route("/", methods=["POST"])
@admin_required
def create_product():
    """POST /api/v1/products/ — Admin: create product."""
    data = request.get_json()
    result, err = ProductService.create(data or {})
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Product created", 201)


@products_bp.route("/<int:product_id>", methods=["PUT"])
@admin_required
def update_product(product_id):
    """PUT /api/v1/products/<id> — Admin."""
    data = request.get_json()
    result, err = ProductService.update(product_id, data or {})
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Product updated")


@products_bp.route("/<int:product_id>", methods=["DELETE"])
@admin_required
def delete_product(product_id):
    """DELETE /api/v1/products/<id> — Admin (soft delete)."""
    _, err = ProductService.delete(product_id)
    if err:
        return error_response(err, 400)
    return success_response({}, "Product deleted")


@products_bp.route("/<int:product_id>/images", methods=["POST"])
@admin_required
def upload_product_image(product_id):
    """POST /api/v1/products/<id>/images — Admin: upload image."""
    if "image" not in request.files:
        # Accept JSON image_url too
        data = request.get_json()
        if data and data.get("image_url"):
            result, err = ProductService.add_image(
                product_id,
                data["image_url"],
                is_primary=data.get("is_primary", False),
                alt_text=data.get("alt_text"),
            )
            if err:
                return error_response(err, 400)
            return success_response(result, "Image added", 201)
        return error_response("No image file or image_url provided", 400)

    file = request.files["image"]
    try:
        url = save_file(file, subfolder="products")
    except ValueError as e:
        return error_response(str(e), 400)

    is_primary = request.form.get("is_primary", "false").lower() == "true"
    alt_text = request.form.get("alt_text")
    result, err = ProductService.add_image(product_id, url, is_primary=is_primary, alt_text=alt_text)
    if err:
        return error_response(err, 400)
    return success_response(result, "Image uploaded", 201)


@products_bp.route("/<int:product_id>/images/<int:image_id>", methods=["DELETE"])
@admin_required
def delete_product_image(product_id, image_id):
    """DELETE /api/v1/products/<id>/images/<image_id>"""
    _, err = ProductService.delete_image(product_id, image_id)
    if err:
        return error_response(err, 404)
    return success_response({}, "Image deleted")


@products_bp.route("/<int:product_id>/variants", methods=["POST"])
@admin_required
def add_product_variant(product_id):
    """POST /api/v1/products/<id>/variants — Admin: add variant."""
    data = request.get_json()
    result, err = ProductService.add_variant(product_id, data or {})
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Variant added", 201)


@products_bp.route("/<int:product_id>/variants/<int:variant_id>", methods=["DELETE"])
@admin_required
def delete_product_variant(product_id, variant_id):
    """DELETE /api/v1/products/<id>/variants/<variant_id>"""
    _, err = ProductService.delete_variant(product_id, variant_id)
    if err:
        return error_response(err, 404)
    return success_response({}, "Variant deleted")
