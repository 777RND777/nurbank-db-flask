def test_create_user(client, user):
    response = client.post("/users", json=user)
    assert response.status_code == 200

    response = client.post("/users", json=user)
    assert response.status_code == 400


def test_get_user(client, user):
    response = client.get(f"/users/{user['_id']}")
    assert response.status_code == 404

    response = client.post("/users", json=user)
    assert response.status_code == 200

    response = client.get(f"/users/{user['_id']}")
    assert response.status_code == 200


def test_get_user_applications_empty(client, user):
    response = client.get(f"/users/{user['_id']}/applications")
    assert response.status_code == 404

    response = client.post("/users", json=user)
    assert response.status_code == 200

    response = client.get(f"/users/{user['_id']}/applications")
    assert response.status_code == 200
    assert len(response.json) == 0


def test_get_user_pending_empty(client, user):
    response = client.get(f"/users/{user['_id']}/pending")
    assert response.status_code == 404

    response = client.post("/users", json=user)
    assert response.status_code == 200

    response = client.get(f"/users/{user['_id']}/pending")
    assert response.status_code == 204
