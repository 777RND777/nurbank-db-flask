from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs

from bank import docs
from bank.auth import check_user
from bank.models import Application, User
from bank.schemas import ApplicationSchema, UserSchema, UserSchemaCreate

users = Blueprint("users", __name__)


@users.route("/users", methods=["POST"])
@use_kwargs(UserSchemaCreate)
@marshal_with(UserSchema)
def create_user(**kwargs):
    kwargs['nickname'] = kwargs['username']
    kwargs['password_hash'] = kwargs.pop('password')

    user = User(**kwargs)
    user.save()
    return user


@users.route("/users", methods=["GET"])
@marshal_with(UserSchema(many=True))
def get_user_list() -> list:
    return User.get_list()


@users.route("/users/<int:user_id>/applications", methods=["GET"])
@check_user
@marshal_with(ApplicationSchema(many=True))
def get_user_applications(user_id: int):
    return Application.get_user_list(user_id)


@users.route("/users/<int:user_id>", methods=["GET"])
@marshal_with(UserSchema)
def get_user(user_id: int):
    return User.get(user_id)


@users.route("/users/<int:user_id>", methods=["PUT"])
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
def update_user(user_id: int, **kwargs):
    user = User.get(user_id)
    if not user:
        return None
    user.update(**kwargs)
    return user


@users.route("/users/<int:user_id>", methods=["DELETE"])
@marshal_with(UserSchema)
def remove_user(user_id: int):
    user = User.get(user_id)
    if not user:
        return None
    user.delete()
    return user


docs.register(get_user_list, blueprint="users")
docs.register(get_user, blueprint="users")
docs.register(get_user_applications, blueprint="users")
docs.register(create_user, blueprint="users")
docs.register(update_user, blueprint="users")
docs.register(remove_user, blueprint="users")
