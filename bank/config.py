from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', '')

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URL', 'sqlite:///db.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False

APISPEC_SPEC = APISpec(title="bank",
                       version="v1",
                       openapi_version="2.0",
                       plugins=[MarshmallowPlugin()])
APISPEC_SWAGGER_URL = "/swagger/"
