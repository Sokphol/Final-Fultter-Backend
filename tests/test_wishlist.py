def test_wishlist_flow(client, auth_headers, admin_headers):
    # Create product
    p_res = client.post("/api/v1/products/", json={
        "name": "Wishlist Test Product",
        "price": 120.0,
        "stock_quantity": 10,
    }, headers=admin_headers)
    p_id = p_res.get_json()["data"]["id"]

    # Add to wishlist
    add_res = client.post(f"/api/v1/wishlist/{p_id}", headers=auth_headers)
    assert add_res.status_code == 201

    # Check
    check_res = client.get(f"/api/v1/wishlist/{p_id}/check", headers=auth_headers)
    assert check_res.status_code == 200
    assert check_res.get_json()["data"]["in_wishlist"] is True

    # Remove
    del_res = client.delete(f"/api/v1/wishlist/{p_id}", headers=auth_headers)
    assert del_res.status_code == 200

