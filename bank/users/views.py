from flask import Blueprint, jsonify
from flask_apispec import use_kwargs

from bank import docs
from bank.auth import check_user, hash_password
from bank.models import Application, User
from bank.schemas import UserSchema, UserSchemaCreate

users = Blueprint("users", __name__)


@users.route("/users", methods=["POST"])
@use_kwargs(UserSchemaCreate)
def create_user(**kwargs) -> (dict, int):
    if User.get(kwargs['_id']):
        return {}, 400

    kwargs['nickname'] = kwargs['username']
    kwargs['password_hash'] = hash_password(kwargs.pop('password'))

    user = User(**kwargs)
    user.save()
    return user.json, 200


@users.route("/users", methods=["GET"])
def get_user_list() -> (list, int):
    return jsonify([x.json for x in User.get_list()]), 200


@users.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int) -> (dict, int):
    user = User.get(user_id)
    if not user:
        return {}, 404

    return user.json, 200


@users.route("/users/<int:user_id>/applications", methods=["GET"])
def get_user_applications(user_id: int) -> (list, int):
    if not User.get(user_id):
        return [], 404

    return jsonify([x.json for x in Application.get_user_list(user_id)]), 200


@users.route("/users/<int:user_id>/pending", methods=["GET"])
def get_user_pending(user_id: int) -> (dict, int):
    if not User.get(user_id):
        return {}, 404

    applications = Application.get_user_list(user_id)
    if len(applications) == 0 or len(applications[-1].answer_date) > 0:
        return {}, 204

    return applications[-1].json, 200


@users.route("/users/<int:user_id>", methods=["PUT"])
@use_kwargs(UserSchema)
@check_user
def update_user(user_id: int, **kwargs) -> (dict, int):
    user = User.get(user_id)
    # no check because of check_user func
    user.update(**kwargs)
    return user.json, 201


docs.register(get_user_list, blueprint="users")
docs.register(get_user, blueprint="users")
docs.register(get_user_applications, blueprint="users")
docs.register(get_user_pending, blueprint="users")
docs.register(create_user, blueprint="users")
docs.register(update_user, blueprint="users")
