def test_get_categories_public(client):
    res = client.get("/api/v1/categories/")
    assert res.status_code == 200
    assert res.get_json()["success"] is True


def test_create_category_admin_only(client, auth_headers):
    res = client.post("/api/v1/categories/", json={"name": "Test Cat"}, headers=auth_headers)
    assert res.status_code == 403


def test_create_category_as_admin(client, admin_headers):
    res = client.post("/api/v1/categories/", json={
        "name": "Test Category",
        "description": "A test category",
    }, headers=admin_headers)
    assert res.status_code == 201
    data = res.get_json()["data"]
    assert data["name"] == "Test Category"
    assert data["slug"] == "test-category"

