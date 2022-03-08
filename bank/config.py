from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY', '')
APISPEC_SPEC = APISpec(title="bank",
                       version="v1",
                       openapi_version="2.0",
                       plugins=[MarshmallowPlugin()])
APISPEC_SWAGGER_URL = "/swagger/"
