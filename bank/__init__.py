from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from flask_apispec.extension import FlaskApiSpec
from .database import *

app = Flask(__name__)
app.config.update({
    "APISPEC_SPEC": APISpec(title="bank",
                            version="v1",
                            openapi_version="2.0",
                            plugins=[MarshmallowPlugin()]),
    "APISPEC_SWAGGER_URL": "/swagger/"
})

init_db()
docs = FlaskApiSpec()

# importing here because of circular import error
from .applications.views import applications
from .users.views import users
app.register_blueprint(applications)
app.register_blueprint(users)

# setting here to include blueprints
docs.init_app(app)
