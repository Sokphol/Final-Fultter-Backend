def test_reviews_flow(client, auth_headers, admin_headers):
    # Create product
    p_res = client.post("/api/v1/products/", json={
        "name": "Review Test Product",
        "price": 89.0,
        "stock_quantity": 10,
    }, headers=admin_headers)
    p_id = p_res.get_json()["data"]["id"]

    # Submit review
    r_res = client.post("/api/v1/reviews/", json={
        "product_id": p_id,
        "rating": 5,
        "title": "Amazing bass!",
        "body": "These headphones sound crisp and deep.",
    }, headers=auth_headers)
    assert r_res.status_code == 201

    # Get reviews
    list_res = client.get(f"/api/v1/reviews/product/{p_id}")
    assert list_res.status_code == 200
    assert len(list_res.get_json()["data"]["items"]) == 1

    # Summary
    summary_res = client.get(f"/api/v1/reviews/product/{p_id}/summary")
    assert summary_res.status_code == 200
    assert summary_res.get_json()["data"]["average"] == 5.0

