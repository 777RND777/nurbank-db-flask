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


def test_get_user_applications(client, user, application):
    response = client.get(f"/users/{user['_id']}/applications")
    assert response.status_code == 404

    response = client.post("/users", json=user)
    assert response.status_code == 200

    response = client.get(f"/users/{user['_id']}/applications")
    assert response.status_code == 200
    assert len(response.json) == 0

    response = client.post("/applications", json=application)
    assert response.status_code == 200
    response = client.post("/applications", json=application)
    assert response.status_code == 200
    response = client.post("/applications", json=application)
    assert response.status_code == 200

    response = client.get(f"/users/{user['_id']}/applications")
    assert response.status_code == 200
    assert len(response.json) == 3


def test_get_user_pending(client, user, application, auth):
    response = client.get(f"/users/{user['_id']}/pending")
    assert response.status_code == 404

    response = client.post("/users", json=user)
    assert response.status_code == 200

    response = client.get(f"/users/{user['_id']}/pending")
    assert response.status_code == 204

    response = client.post("/applications", json=application)
    assert response.status_code == 200
    application_id = response.json['_id']

    response = client.get(f"/users/{user['_id']}/pending")
    assert response.status_code == 200

    response = client.put(f"/applications/{application_id}/decline", json=auth)
    assert response.status_code == 201

    response = client.get(f"/users/{user['_id']}/pending")
    assert response.status_code == 204
