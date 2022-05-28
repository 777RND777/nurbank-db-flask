from bank import db
from bank.auth import hash_password
from bank.models import User


def create_user(kwargs) -> User:
    kwargs['nickname'] = kwargs['username']
    kwargs['password'] = hash_password(kwargs['password'])

    user = User(**kwargs)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_list() -> list[User]:
    return [x for x in User.query.all()]


def get_user(user_id: int) -> User:
    return User.query.filter(User.id_ == user_id).first()


def update_user(user: User, **kwargs):
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.session.commit()
