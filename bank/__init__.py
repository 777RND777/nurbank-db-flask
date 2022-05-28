from flask import Flask
from flask_apispec.extension import FlaskApiSpec
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
docs = FlaskApiSpec()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # importing here because of circular import error
    from .applications.views import applications
    from .users.views import users
    app.register_blueprint(applications)
    app.register_blueprint(users)

    # setting here to include blueprints
    db.init_app(app)
    with app.app_context():
        db.create_all()
    docs.init_app(app)

    return app
