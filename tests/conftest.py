import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        yield _db
        _db.session.rollback()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Returns JWT headers for a registered test user."""
    client.post("/api/v1/auth/register", json={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "password123",
    })
    res = client.post("/api/v1/auth/login", json={
        "email": "testuser@example.com",
        "password": "password123",
    })
    token = res.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client, app):
    """Returns JWT headers for an admin user."""
    from app.models.user import User
    from app.models.cart import Cart
    from app.utils.security import hash_password
    with app.app_context():
        user = User.query.filter_by(email="admin@test.com").first()
        if not user:
            user = User(
                name="Admin",
                email="admin@test.com",
                password_hash=hash_password("adminpass"),
                role="admin",
            )
            _db.session.add(user)
            _db.session.flush()
            cart = Cart(user_id=user.id)
            _db.session.add(cart)
            _db.session.commit()

    res = client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "adminpass",
    })
    token = res.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}
