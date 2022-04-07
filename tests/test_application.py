def test_create_application(client, user, application):
    response = client.post("/users", json=user)
    assert response.status_code == 200

    response = client.post("/applications", json=application)
    assert response.status_code == 200


def test_get_application(client, user, application):
    response = client.post("/users", json=user)
    assert response.status_code == 200

    response = client.post("/applications", json=application)
    assert response.status_code == 200
    application_id = response.json['_id']

    response = client.get(f"/applications/{application_id}")
    assert response.status_code == 200


def test_approve_application(client, user, application, auth):
    response = client.post("/users", json=user)
    assert response.status_code == 200
    start_debt = response.json['debt']

    response = client.post("/applications", json=application)
    assert response.status_code == 200
    application_id = response.json['_id']

    wrong_auth = {"user_id": auth['user_id'], "password": "wrong_password"}
    response = client.put(f"/applications/{application_id}/approve", json=wrong_auth)
    assert response.status_code == 401

    response = client.put(f"/applications/{application_id}/approve", json=auth)
    assert response.status_code == 201

    response = client.put(f"/applications/{application_id}/approve", json=auth)
    assert response.status_code == 204

    response = client.get(f"/users/{application['user_id']}")
    assert response.status_code == 200
    assert response.json['debt'] == start_debt + application['value']


def test_decline_application(client, user, application, auth):
    response = client.post("/users", json=user)
    assert response.status_code == 200
    start_debt = response.json['debt']

    response = client.post("/applications", json=application)
    assert response.status_code == 200
    application_id = response.json['_id']

    wrong_auth = {"user_id": auth['user_id'], "password": "wrong_password"}
    response = client.put(f"/applications/{application_id}/decline", json=wrong_auth)
    assert response.status_code == 401

    response = client.put(f"/applications/{application_id}/decline", json=auth)
    assert response.status_code == 201

    response = client.put(f"/applications/{application_id}/decline", json=auth)
    assert response.status_code == 204

    response = client.get(f"/users/{application['user_id']}")
    assert response.status_code == 200
    assert response.json['debt'] == start_debt
