from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs

from bank import docs
from bank.auth import auth
from bank.models import Application
from bank.schemas import ApplicationSchema, ApplicationSchemaBase, ApplicationSchemaCreate, ApplicationSchemaOutput
from . import crud

applications = Blueprint("applications", __name__)


@applications.post("/applications")
@use_kwargs(ApplicationSchemaCreate)
@marshal_with(ApplicationSchemaOutput)
@auth
def create_application(**kwargs) -> (Application, int):
    return crud.create_application(**kwargs), 200


@applications.get("/applications/<int:application_id>")
@marshal_with(ApplicationSchemaOutput)
def get_application(application_id: int) -> (Application, int):
    application = crud.get_application(application_id)
    if not application:
        return None, 404

    return application, 200


@applications.put("/applications/<int:application_id>")
@use_kwargs(ApplicationSchema)
@marshal_with(ApplicationSchemaOutput)
@auth
def update_application(application_id: int, **kwargs) -> (Application, int):
    application = crud.get_application(application_id)
    if not application:
        return None, 404

    crud.update_application(application, **kwargs)
    return application, 201


@applications.put("/applications/<int:application_id>/approve")
@use_kwargs(ApplicationSchemaBase)
@marshal_with(ApplicationSchemaOutput)
@auth
def approve_application(application_id: int, **_) -> (Application, int):
    application = crud.get_application(application_id)
    if not application:
        return None, 404
    if len(application.answer_date) > 0:
        return None, 204

    crud.approve_application(application)
    return application, 201


@applications.put("/applications/<int:application_id>/decline")
@use_kwargs(ApplicationSchemaBase)
@marshal_with(ApplicationSchemaOutput)
@auth
def decline_application(application_id: int, **_) -> (Application, int):
    application = crud.get_application(application_id)
    if not application:
        return None, 404
    if len(application.answer_date) > 0:
        return None, 204

    crud.decline_application(application)
    return application, 201


docs.register(create_application, blueprint="applications")
docs.register(get_application, blueprint="applications")
docs.register(approve_application, blueprint="applications")
docs.register(decline_application, blueprint="applications")
