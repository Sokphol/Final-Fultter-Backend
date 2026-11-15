def test_get_products_public(client):
    res = client.get("/api/v1/products/")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "pagination" in data["data"]


def test_get_featured(client):
    res = client.get("/api/v1/products/featured")
    assert res.status_code == 200


def test_create_product_requires_admin(client, auth_headers):
    res = client.post("/api/v1/products/", json={"name": "Test"}, headers=auth_headers)
    assert res.status_code == 403


def test_create_and_get_product(client, admin_headers):
    res = client.post("/api/v1/products/", json={
        "name": "Sony Test XM99",
        "price": 299.99,
        "stock_quantity": 10,
        "short_description": "Test headphone",
    }, headers=admin_headers)
    assert res.status_code == 201
    product_id = res.get_json()["data"]["id"]

    res2 = client.get(f"/api/v1/products/{product_id}")
    assert res2.status_code == 200
    assert res2.get_json()["data"]["name"] == "Sony Test XM99"

