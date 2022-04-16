from flask import Blueprint
from flask_apispec import use_kwargs

from bank import docs
from bank.auth import auth
from bank.schemas import ApplicationSchema, ApplicationSchemaBase, ApplicationSchemaCreate
from . import crud

applications = Blueprint("applications", __name__)


@applications.route("/applications", methods=["POST"])
@use_kwargs(ApplicationSchemaCreate)
@auth
def create_application(**kwargs) -> (dict, int):
    return crud.create_application(**kwargs).json, 200


@applications.route("/applications/<int:application_id>", methods=["GET"])
def get_application(application_id: int) -> (dict, int):
    application = crud.get_application(application_id)
    if not application:
        return {}, 404

    return application.json, 200


@applications.route("/applications/<int:application_id>", methods=["PUT"])
@use_kwargs(ApplicationSchema)
@auth
def update_application(application_id: int, **kwargs) -> (dict, int):
    application = crud.get_application(application_id)
    if not application:
        return {}, 404

    crud.update_application(application, **kwargs)
    return application.json, 201


@applications.route("/applications/<int:application_id>/approve", methods=["PUT"])
@use_kwargs(ApplicationSchemaBase)
@auth
def approve_application(application_id: int, **_) -> (dict, int):
    application = crud.get_application(application_id)
    if not application:
        return {}, 404
    if len(application.answer_date) > 0:
        return {}, 204

    crud.approve_application(application)
    return application.json, 201


@applications.route("/applications/<int:application_id>/decline", methods=["PUT"])
@use_kwargs(ApplicationSchemaBase)
@auth
def decline_application(application_id: int, **_) -> (dict, int):
    application = crud.get_application(application_id)
    if not application:
        return {}, 404
    if len(application.answer_date) > 0:
        return {}, 204

    crud.decline_application(application)
    return application.json, 201


docs.register(create_application, blueprint="applications")
docs.register(get_application, blueprint="applications")
docs.register(approve_application, blueprint="applications")
docs.register(decline_application, blueprint="applications")
