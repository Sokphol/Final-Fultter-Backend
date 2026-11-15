def test_get_addresses(client, auth_headers):
    res = client.get("/api/v1/addresses/", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["success"] is True


def test_create_and_delete_address(client, auth_headers):
    res = client.post("/api/v1/addresses/", json={
        "full_name": "Test Receiver",
        "phone": "+85512345678",
        "street": "Street 2004",
        "city": "Phnom Penh",
        "country": "Cambodia",
        "is_default": True,
    }, headers=auth_headers)
    assert res.status_code == 201
    addr_id = res.get_json()["data"]["id"]

    del_res = client.delete(f"/api/v1/addresses/{addr_id}", headers=auth_headers)
    assert del_res.status_code == 200

