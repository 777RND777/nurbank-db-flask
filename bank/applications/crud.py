from bank import db
from bank.models import Application, User
from .helpers import get_current_time, get_unique_id


def create_application(**kwargs) -> Application:
    kwargs['id_'] = get_unique_id()
    kwargs['request_date'] = get_current_time()

    application = Application(**kwargs)
    db.session.add(application)
    db.session.commit()
    return application


def get_application(application_id: int) -> Application:
    application = Application.query.filter(Application.id_ == application_id).first()
    return application


def update_application(application: Application, **kwargs):
    for key, value in kwargs.items():
        setattr(application, key, value)
    db.session.commit()


def approve_application(application: Application):
    application.answer_date = get_current_time()
    application.approved = True
    db.session.commit()

    user = User.get(application.user_id)
    # no check because of auth func
    user.debt += application.value
    db.session.commit()


def decline_application(application: Application):
    application.answer_date = get_current_time()
    db.session.commit()
