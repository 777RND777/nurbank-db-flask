from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs

from bank import docs
from bank.auth import check_user
from bank.models import Application, User
from bank.schemas import ApplicationSchema, ApplicationSchemaBase, ApplicationSchemaCreate
from .helpers import get_current_time

applications = Blueprint("applications", __name__)


@applications.route("/applications", methods=["POST"])
@use_kwargs(ApplicationSchemaCreate)
@check_user
@marshal_with(ApplicationSchema)
def create_application(**kwargs):
    kwargs['request_date'] = get_current_time()
    application = Application(**kwargs)
    application.save()
    return application


@applications.route("/applications/<int:application_id>", methods=["GET"])
@marshal_with(ApplicationSchema)
def get_application(application_id: int):
    return Application.get(application_id)


@applications.route("/applications/<int:application_id>/approve", methods=["PUT"])
@use_kwargs(ApplicationSchemaBase)
@check_user
@marshal_with(ApplicationSchema)
def approve_application(application_id: int, **_):
    application = Application.get(application_id)
    # TODO messages
    if not application:
        return application
    if len(application.answer_date) > 0:
        return application

    application.answer_date = get_current_time()
    application.approved = True
    application.save()

    user = User.get(application.user_id)
    user.debt += application.value
    user.save()

    return application


@applications.route("/applications/<int:application_id>/decline", methods=["PUT"])
@use_kwargs(ApplicationSchemaBase)
@check_user
@marshal_with(ApplicationSchema)
def decline_application(application_id: int, **_):
    application = Application.get(application_id)
    # TODO messages
    if not application:
        return application
    if len(application.answer_date) > 0:
        return application

    application.answer_date = get_current_time()
    application.save()
    return application


docs.register(create_application, blueprint="applications")
docs.register(get_application, blueprint="applications")
docs.register(approve_application, blueprint="applications")
docs.register(decline_application, blueprint="applications")
