from bcrypt import gensalt, hashpw

from bank.models import User


def hash_password(password: str) -> bytes:
    password_bytes = password.encode('utf-8')
    hashed_password = hashpw(password_bytes, gensalt())
    return hashed_password


def check_password(password: str, hashed_password: bytes):
    password = password.encode('utf-8')
    return hashpw(password, hashed_password) == hashed_password


def auth(func) -> (dict, int):
    def wrapper(**kwargs):
        user = User.get(kwargs['user_id'])
        if not user:
            return {}, 401

        if not check_password(kwargs.pop('password'), user.hashed_password):
            return {}, 401

        return func(**kwargs)

    wrapper.__name__ = func.__name__
    return wrapper
