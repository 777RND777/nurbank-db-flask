from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs

from bank import docs
from bank.models import User
from bank.schemas import UserSchema, UserSchemaCreate

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    pass


@auth.route("/login", methods=["POST"])
def login():
    pass
