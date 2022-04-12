from bank import create_app, db
import os
import pytest


@pytest.fixture()
def client():
    app = create_app()
    app.config['TESTING'] = True
    path = "test_db.sqlite"

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///../tests/{path}"

    db.init_app(app)
    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    if not os.getcwd().endswith("tests"):
        # run is not from test dir (e.g. from terminal)
        path = os.path.join("tests", path)
    os.remove(path)


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
def nickname():
    return "nickname"


@pytest.fixture()
def n():
    return 3
