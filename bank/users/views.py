from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs

from bank import docs
from bank.auth import check_password
from bank.models import Application, User
from bank.schemas import ApplicationSchemaOutput, UserSchema, UserSchemaCreate, UserSchemaOutput
from . import crud

users = Blueprint("users", __name__)


@users.post("/users")
@use_kwargs(UserSchemaCreate)
@marshal_with(UserSchemaOutput)
def create_user(**kwargs) -> (User, int):
    if crud.get_user(kwargs['id_']):
        return None, 400

    return crud.create_user(kwargs), 200


@users.get("/users")
@marshal_with(UserSchemaOutput(many=True))
def get_user_list() -> (list[User], int):
    return crud.get_user_list(), 200


@users.get("/users/<int:user_id>")
@marshal_with(UserSchemaOutput)
def get_user(user_id: int) -> (User, int):
    user = crud.get_user(user_id)
    # if not user:
    #     return None, 404

    return user, 200


@users.get("/users/<int:user_id>/applications")
@marshal_with(ApplicationSchemaOutput(many=True))
def get_user_applications(user_id: int) -> (list[Application], int):
    user = crud.get_user(user_id)
    if not user:
        return None, 404

    return [x for x in user.applications], 200


@users.get("/users/<int:user_id>/pending")
@marshal_with(ApplicationSchemaOutput)
def get_user_pending(user_id: int) -> (Application, int):
    user = crud.get_user(user_id)
    if not user:
        return None, 404

    applications = user.applications
    if len(applications) == 0 or len(applications[-1].answer_date) > 0:
        return None, 204

    return applications[-1], 200


@users.put("/users/<int:user_id>")
@use_kwargs(UserSchema)
@marshal_with(UserSchemaOutput)
def update_user(user_id: int, password: str, **kwargs) -> (User, int):
    user = crud.get_user(user_id)
    if not user:
        return None, 404

    if not check_password(password, user.password):
        return None, 401

    crud.update_user(user, **kwargs)
    return user, 201


docs.register(get_user_list, blueprint="users")
docs.register(get_user, blueprint="users")
docs.register(get_user_applications, blueprint="users")
docs.register(get_user_pending, blueprint="users")
docs.register(create_user, blueprint="users")
docs.register(update_user, blueprint="users")
