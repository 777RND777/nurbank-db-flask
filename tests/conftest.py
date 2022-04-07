from bank import create_app, db
import os
import pytest


@pytest.fixture()
def client():
    app = create_app()
    app.config['TESTING'] = True
    name = "fake_db.sqlite"
    path = f"../bank/{name}" if os.getcwd().endswith("tests") else name

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{path}"

    db.init_app(app)
    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    os.remove(os.path.join("bank", name))


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
def n():
    return 3
