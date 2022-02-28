from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs

from bank import docs
from bank.models import Application
from bank.schemas import ApplicationSchema

applications = Blueprint("applications", __name__)


@applications.route("/applications", methods=["POST"])
@marshal_with(ApplicationSchema)
@use_kwargs(ApplicationSchema)
def create_application(**kwargs):
    application = Application(**kwargs)
    application.save()
    return application


@applications.route("/applications", methods=["GET"])
@marshal_with(ApplicationSchema(many=True))
def get_application_list() -> list:
    return Application.get_list()


@applications.route("/applications/<int:application_id>", methods=["GET"])
@marshal_with(ApplicationSchema)
def get_application(application_id: int):
    return Application.get(application_id)


@applications.route("/applications/<int:application_id>", methods=["PUT"])
@marshal_with(ApplicationSchema)
@use_kwargs(ApplicationSchema)
def update_application(application_id: int, **kwargs):
    application = Application.get(application_id)
    application.update(**kwargs)
    return application


@applications.route("/applications/<int:application_id>", methods=["DELETE"])
@marshal_with(ApplicationSchema)
def remove_application(application_id: int) -> (str, int):
    application = Application.get(application_id)
    application.delete()
    return "", 204


docs.register(get_application_list, blueprint="applications")
docs.register(create_application, blueprint="applications")
docs.register(update_application, blueprint="applications")
docs.register(remove_application, blueprint="applications")
