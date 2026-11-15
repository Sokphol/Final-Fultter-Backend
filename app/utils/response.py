from flask import jsonify
from typing import Any, Optional


def success_response(data: Any = None, message: str = "Success", status_code: int = 200):
    """Standardized success JSON response."""
    return jsonify({
        "success": True,
        "message": message,
        "data": data,
    }), status_code


def error_response(message: str = "Error", status_code: int = 400, errors: Optional[dict] = None):
    """Standardized error JSON response."""
    body = {
        "success": False,
        "message": message,
        "data": None,
    }
    if errors:
        body["errors"] = errors
    return jsonify(body), status_code


def paginated_response(items: list, total: int, page: int, per_page: int, message: str = "Success"):
    """Standardized paginated JSON response."""
    import math
    return jsonify({
        "success": True,
        "message": message,
        "data": {
            "items": items,
            "pagination": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": math.ceil(total / per_page) if per_page else 1,
                "has_next": page * per_page < total,
                "has_prev": page > 1,
            }
        }
    }), 200
