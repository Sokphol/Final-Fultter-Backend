def test_get_cart_empty(client, auth_headers):
    res = client.get("/api/v1/cart/", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["data"]["items"] == []


def test_add_to_cart(client, auth_headers, admin_headers):
    # Create product first
    p_res = client.post("/api/v1/products/", json={
        "name": "Cart Test Headphone",
        "price": 99.99,
        "stock_quantity": 5,
    }, headers=admin_headers)
    product_id = p_res.get_json()["data"]["id"]

    res = client.post("/api/v1/cart/items", json={
        "product_id": product_id,
        "quantity": 2,
    }, headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 2


def test_add_to_cart_requires_auth(client):
    res = client.post("/api/v1/cart/items", json={"product_id": 1, "quantity": 1})
    assert res.status_code == 401

