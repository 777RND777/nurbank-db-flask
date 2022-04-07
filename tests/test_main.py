def test_user(client, user):
    response = client.get(f"/users/{user['_id']}")
    assert response.status_code == 404

    response = client.post("/users", json=user)
    assert response.status_code == 200

    response = client.get(f"/users/{user['_id']}")
    assert response.status_code == 200

    response = client.post("/users", json=user)
    assert response.status_code == 400

    body = {"password": user['password'], "nickname": "nickname"}
    response = client.put(f"/users/{user['_id']}", json=body)
    assert response.status_code == 201


def test_application(client, user, application, auth):
    response = client.post("/users", json=user)
    assert response.status_code == 200

    response = client.get(f"/users/{application['user_id']}/applications")
    assert response.status_code == 200

    # decline
    response = client.post("/applications", json=application)
    assert response.status_code == 200

    response = client.get(f"/users/{application['user_id']}/pending")
    assert response.status_code == 200
    application_id = response.json['_id']

    response = client.put(f"/applications/{application_id}/decline", json=auth)
    assert response.status_code == 201

    response = client.get(f"/users/{application['user_id']}/pending")
    assert response.status_code == 204

    response = client.put(f"/applications/{application_id}/decline", json=auth)
    assert response.status_code == 204

    response = client.get(f"/users/{application['user_id']}")
    assert response.json['debt'] == 0

    # approve
    response = client.post("/applications", json=application)
    assert response.status_code == 200

    response = client.get(f"/users/{application['user_id']}/pending")
    assert response.status_code == 200
    application_id = response.json['_id']

    response = client.put(f"/applications/{application_id}/approve", json=auth)
    assert response.status_code == 201

    response = client.put(f"/applications/{application_id}/approve", json=auth)
    assert response.status_code == 204

    response = client.get(f"/users/{application['user_id']}")
    assert application['value'] == response.json['debt']
