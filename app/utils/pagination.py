from flask import request


def get_pagination_params():
    """Extract pagination params from request query string."""
    try:
        page = max(1, int(request.args.get("page", 1)))
    except (ValueError, TypeError):
        page = 1
    try:
        per_page = min(100, max(1, int(request.args.get("per_page", 12))))
    except (ValueError, TypeError):
        per_page = 12
    return page, per_page


def paginate_query(query, page: int, per_page: int):
    """Paginate a SQLAlchemy query."""
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return pagination.items, pagination.total
