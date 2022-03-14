from bcrypt import gensalt, hashpw

from bank.models import User


def hash_password(password: str) -> bytes:
    password_bytes = password.encode('utf-8')
    hashed_password = hashpw(password_bytes, gensalt())
    return hashed_password


def check_user(func):
    def wrapper(**kwargs):
        user = User.get(kwargs['user_id'])
        if not user:
            return

        password = kwargs['password'].encode('utf-8')
        if hashpw(password, user.password_hash) != user.password_hash:
            return

        kwargs.pop('password')
        return func(**kwargs)

    wrapper.__name__ = func.__name__
    return wrapper
