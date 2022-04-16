from flask import Blueprint, jsonify, Response
from flask_apispec import use_kwargs

from bank import docs
from bank.auth import check_password
from bank.schemas import UserSchema, UserSchemaCreate
from . import crud

users = Blueprint("users", __name__)


@users.route("/users", methods=["POST"])
@use_kwargs(UserSchemaCreate)
def create_user(**kwargs) -> (dict, int):
    if crud.get_user(kwargs['_id']):
        return {}, 400

    return crud.create_user(kwargs).json, 200


@users.route("/users", methods=["GET"])
def get_user_list() -> (Response, int):
    return jsonify(crud.get_user_list()), 200


@users.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int) -> (dict, int):
    user = crud.get_user(user_id)
    if not user:
        return {}, 404

    return user.json, 200


@users.route("/users/<int:user_id>/applications", methods=["GET"])
def get_user_applications(user_id: int) -> (Response, int):
    user = crud.get_user(user_id)
    if not user:
        return jsonify([]), 404

    return jsonify([x.json for x in user.applications]), 200


@users.route("/users/<int:user_id>/pending", methods=["GET"])
def get_user_pending(user_id: int) -> (dict, int):
    user = crud.get_user(user_id)
    if not user:
        return {}, 404

    applications = user.applications
    if len(applications) == 0 or len(applications[-1].answer_date) > 0:
        return {}, 204

    return applications[-1].json, 200


@users.route("/users/<int:user_id>", methods=["PUT"])
@use_kwargs(UserSchema)
def update_user(user_id: int, password: str, **kwargs) -> (dict, int):
    user = crud.get_user(user_id)
    if not user:
        return {}, 404

    if not check_password(password, user.password):
        return {}, 401

    crud.update_user(user, **kwargs)
    return user.json, 201


docs.register(get_user_list, blueprint="users")
docs.register(get_user, blueprint="users")
docs.register(get_user_applications, blueprint="users")
docs.register(get_user_pending, blueprint="users")
docs.register(create_user, blueprint="users")
docs.register(update_user, blueprint="users")
