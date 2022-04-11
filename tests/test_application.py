def test_create_application(client, user, application):
    response = client.post("/users", json=user)
    assert response.status_code == 200

    response = client.post("/applications", json=application)
    assert response.status_code == 200

    application['value2'] = 0
    response = client.post("/applications", json=application)
    assert response.status_code == 422
    del application['value2']

    application.pop("value")
    response = client.post("/applications", json=application)
    assert response.status_code == 422


def test_get_application(client, user, application):
    response = client.post("/users", json=user)
    assert response.status_code == 200

    response = client.post("/applications", json=application)
    assert response.status_code == 200
    application_id = response.json['_id']

    response = client.get(f"/applications/{application_id}")
    assert response.status_code == 200


def test_update_application(client, user, application):
    response = client.post("/users", json=user)
    assert response.status_code == 200

    response = client.post("/applications", json=application)
    assert response.status_code == 200
    application_id = response.json['_id']

    auth = {"user_id": user['_id'], "password": user['password'], "password2": ""}
    response = client.put(f"/applications/{application_id}", json=auth)
    assert response.status_code == 422

    auth = {"user_id": user['_id']}
    response = client.put(f"/applications/{application_id}", json=auth)
    assert response.status_code == 422

    auth = {"user_id": user['_id'], "password": "wrong_password"}
    response = client.put(f"/applications/{application_id}", json=auth)
    assert response.status_code == 401

    auth = {"user_id": user['_id'], "password": user['password'], "value": application['value'] + 1}
    response = client.put(f"/applications/{application_id}", json=auth)
    assert response.status_code == 201

    response = client.get(f"/applications/{application_id}")
    assert response.status_code == 200
    assert response.json['value'] == application['value'] + 1


def test_approve_application(client, user, application):
    response = client.post("/users", json=user)
    assert response.status_code == 200
    start_debt = response.json['debt']

    response = client.post("/applications", json=application)
    assert response.status_code == 200
    application_id = response.json['_id']

    auth = {"user_id": user['_id'], "password": user['password'], "password2": ""}
    response = client.put(f"/applications/{application_id}/approve", json=auth)
    assert response.status_code == 422

    auth = {"user_id": user['_id']}
    response = client.put(f"/applications/{application_id}/approve", json=auth)
    assert response.status_code == 422

    auth = {"user_id": user['_id'], "password": "wrong_password"}
    response = client.put(f"/applications/{application_id}/approve", json=auth)
    assert response.status_code == 401

    auth = {"user_id": user['_id'], "password": user['password']}
    response = client.put(f"/applications/{application_id}/approve", json=auth)
    assert response.status_code == 201

    response = client.put(f"/applications/{application_id}/approve", json=auth)
    assert response.status_code == 204

    response = client.get(f"/users/{user['_id']}")
    assert response.status_code == 200
    assert response.json['debt'] == start_debt + application['value']


def test_decline_application(client, user, application):
    response = client.post("/users", json=user)
    assert response.status_code == 200
    start_debt = response.json['debt']

    response = client.post("/applications", json=application)
    assert response.status_code == 200
    application_id = response.json['_id']

    auth = {"user_id": user['_id'], "password": user['password'], "password2": ""}
    response = client.put(f"/applications/{application_id}/decline", json=auth)
    assert response.status_code == 422

    auth = {"user_id": user['_id']}
    response = client.put(f"/applications/{application_id}/decline", json=auth)
    assert response.status_code == 422

    auth = {"user_id": user['_id'], "password": "wrong_password"}
    response = client.put(f"/applications/{application_id}/decline", json=auth)
    assert response.status_code == 401

    auth = {"user_id": user['_id'], "password": user['password']}
    response = client.put(f"/applications/{application_id}/decline", json=auth)
    assert response.status_code == 201

    response = client.put(f"/applications/{application_id}/decline", json=auth)
    assert response.status_code == 204

    response = client.get(f"/users/{user['_id']}")
    assert response.status_code == 200
    assert response.json['debt'] == start_debt
