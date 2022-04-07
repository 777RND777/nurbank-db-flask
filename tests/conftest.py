from bank import create_app, db
import os
import pytest


@pytest.fixture()
def n():
    return 3


@pytest.fixture()
def auth():
    return {
        "user_id": 1,  # named so instead of "_id" because of application requests
        "password": "password"
    }


@pytest.fixture()
def application(auth):
    return {
        "user_id": auth['user_id'],
        "password": auth['password'],
        "value": 200
    }


@pytest.fixture()
def user(auth):
    return {
        "_id": auth['user_id'],
        "password": auth['password'],
        "first_name": "first_name",
        "last_name": "last_name",
        "username": "username"
    }


@pytest.fixture()
def client(auth):
    app = create_app()
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../bank/fake_db.sqlite"

    db.init_app(app)
    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    os.remove(os.path.join("", "..", "bank", "fake_db.sqlite"))
