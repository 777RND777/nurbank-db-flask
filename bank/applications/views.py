from flask import Blueprint
from flask_apispec import use_kwargs

from bank import docs
from bank.auth import check_user
from bank.models import Application, User
from bank.schemas import ApplicationSchemaBase, ApplicationSchemaCreate
from .helpers import get_current_time, get_unique_id

applications = Blueprint("applications", __name__)


@applications.route("/applications", methods=["POST"])
@use_kwargs(ApplicationSchemaCreate)
@check_user
def create_application(**kwargs) -> (dict, int):
    kwargs['_id'] = get_unique_id()
    kwargs['request_date'] = get_current_time()

    application = Application(**kwargs)
    application.save()
    return application.json, 200


@applications.route("/applications/<int:application_id>", methods=["GET"])
def get_application(application_id: int) -> (dict, int):
    application = Application.get(application_id)
    if not application:
        return {}, 404

    return application.json, 200


@applications.route("/applications/<int:application_id>/approve", methods=["PUT"])
@use_kwargs(ApplicationSchemaBase)
@check_user
def approve_application(application_id: int, **_) -> (dict, int):
    application = Application.get(application_id)
    if not application:
        return {}, 404
    if len(application.answer_date) > 0:
        return {}, 204

    application.answer_date = get_current_time()
    application.approved = True
    application.save()

    user = User.get(application.user_id)
    # no check because of check_user func
    user.debt += application.value
    user.save()

    return application.json, 201


@applications.route("/applications/<int:application_id>/decline", methods=["PUT"])
@use_kwargs(ApplicationSchemaBase)
@check_user
def decline_application(application_id: int, **_) -> (dict, int):
    application = Application.get(application_id)
    if not application:
        return {}, 404
    if len(application.answer_date) > 0:
        return {}, 204

    application.answer_date = get_current_time()
    application.save()
    return application.json, 201


docs.register(create_application, blueprint="applications")
docs.register(get_application, blueprint="applications")
docs.register(approve_application, blueprint="applications")
docs.register(decline_application, blueprint="applications")
