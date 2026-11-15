from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.address_service import AddressService
from app.utils.response import success_response, error_response

addresses_bp = Blueprint("addresses", __name__)


@addresses_bp.route("/", methods=["GET"])
@jwt_required()
def get_addresses():
    """GET /api/v1/addresses/ — Get my addresses."""
    result, err = AddressService.get_by_user(get_jwt_identity())
    if err:
        return error_response(err, 400)
    return success_response(result, "Addresses fetched")


@addresses_bp.route("/", methods=["POST"])
@jwt_required()
def create_address():
    """POST /api/v1/addresses/ — Add new address."""
    data = request.get_json()
    if not data:
        return error_response("No data provided", 400)
    result, err = AddressService.create(get_jwt_identity(), data)
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Address created", 201)


@addresses_bp.route("/<int:address_id>", methods=["GET"])
@jwt_required()
def get_address(address_id):
    """GET /api/v1/addresses/<id>"""
    result, err = AddressService.get_by_id(address_id, get_jwt_identity())
    if err:
        return error_response(err, 404)
    return success_response(result, "Address fetched")


@addresses_bp.route("/<int:address_id>", methods=["PUT"])
@jwt_required()
def update_address(address_id):
    """PUT /api/v1/addresses/<id>"""
    data = request.get_json()
    result, err = AddressService.update(address_id, get_jwt_identity(), data or {})
    if err:
        return error_response(str(err), 400)
    return success_response(result, "Address updated")


@addresses_bp.route("/<int:address_id>", methods=["DELETE"])
@jwt_required()
def delete_address(address_id):
    """DELETE /api/v1/addresses/<id>"""
    _, err = AddressService.delete(address_id, get_jwt_identity())
    if err:
        return error_response(err, 400)
    return success_response({}, "Address deleted")


@addresses_bp.route("/<int:address_id>/set-default", methods=["PATCH"])
@jwt_required()
def set_default_address(address_id):
    """PATCH /api/v1/addresses/<id>/set-default"""
    result, err = AddressService.set_default(address_id, get_jwt_identity())
    if err:
        return error_response(err, 400)
    return success_response(result, "Default address updated")
