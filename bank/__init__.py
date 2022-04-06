from flask import Flask
from flask_apispec.extension import FlaskApiSpec

from .database import *

init_db()
docs = FlaskApiSpec()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # importing here because of circular import error
    from .applications.views import applications
    from .users.views import users
    app.register_blueprint(applications)
    app.register_blueprint(users)

    # setting here to include blueprints
    docs.init_app(app)
    return app
