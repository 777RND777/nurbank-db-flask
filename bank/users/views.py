from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs

from bank import docs
from bank.auth import check_user, hash_password
from bank.models import Application, User
from bank.schemas import ApplicationSchema, UserSchema, UserSchemaCreate

users = Blueprint("users", __name__)


@users.route("/users", methods=["POST"])
@use_kwargs(UserSchemaCreate)
@marshal_with(UserSchema)
def create_user(**kwargs):
    kwargs['nickname'] = kwargs['username']
    kwargs['password_hash'] = hash_password(kwargs.pop('password'))

    user = User(**kwargs)
    user.save()
    return user


@users.route("/users", methods=["GET"])
@marshal_with(UserSchema(many=True))
def get_user_list() -> list:
    return User.get_list()


@users.route("/users/<int:user_id>", methods=["GET"])
@marshal_with(UserSchema)
def get_user(user_id: int):
    return User.get(user_id)


@users.route("/users/<int:user_id>/applications", methods=["GET"])
@marshal_with(ApplicationSchema(many=True))
def get_user_applications(user_id: int):
    return Application.get_user_list(user_id)


@users.route("/users/<int:user_id>/pending", methods=["GET"])
@marshal_with(ApplicationSchema)
def get_user_pending(user_id: int):
    applications = Application.get_user_list(user_id)
    # TODO messages
    if len(applications) == 0:
        return None
    if len(applications[-1].answer_date) > 0:
        return None

    return applications[-1]


@users.route("/users/<int:user_id>", methods=["PUT"])
@use_kwargs(UserSchema)
@check_user
@marshal_with(UserSchema)
def update_user(user_id: int, **kwargs):
    user = User.get(user_id)
    # TODO messages
    if not user:
        return None

    user.update(**kwargs)
    return user


docs.register(get_user_list, blueprint="users")
docs.register(get_user, blueprint="users")
docs.register(get_user_applications, blueprint="users")
docs.register(get_user_pending, blueprint="users")
docs.register(create_user, blueprint="users")
docs.register(update_user, blueprint="users")
