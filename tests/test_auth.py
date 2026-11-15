def test_register_success(client):
    res = client.post("/api/v1/auth/register", json={
        "name": "Alice",
        "email": "alice@example.com",
        "password": "securepass",
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert "user" in data["data"]


def test_register_duplicate_email(client):
    payload = {"name": "Bob", "email": "bob@example.com", "password": "pass123"}
    client.post("/api/v1/auth/register", json=payload)
    res = client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 400


def test_login_success(client):
    client.post("/api/v1/auth/register", json={
        "name": "Carol",
        "email": "carol@example.com",
        "password": "mypassword",
    })
    res = client.post("/api/v1/auth/login", json={
        "email": "carol@example.com",
        "password": "mypassword",
    })
    assert res.status_code == 200
    assert "access_token" in res.get_json()["data"]
    assert "refresh_token" in res.get_json()["data"]


def test_login_wrong_password(client):
    client.post("/api/v1/auth/register", json={
        "name": "Dave",
        "email": "dave@example.com",
        "password": "correct",
    })
    res = client.post("/api/v1/auth/login", json={
        "email": "dave@example.com",
        "password": "wrong",
    })
    assert res.status_code == 401


def test_get_me(client, auth_headers):
    res = client.get("/api/v1/auth/me", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["data"]["email"] == "testuser@example.com"


def test_me_requires_auth(client):
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401
