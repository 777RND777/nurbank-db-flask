from bcrypt import gensalt, hashpw

from bank.models import User


def hash_password(password: str) -> bytes:
    password_bytes = password.encode('utf-8')
    hashed_password = hashpw(password_bytes, gensalt())
    return hashed_password


def check_user(func):
    def wrapper(**kwargs):
        user_key = 'user_id' if 'user_id' in kwargs.keys() else 'id'
        user = User.get(kwargs[user_key])
        if not user:
            return

        user_password = kwargs['user_password'].encode('utf-8')
        if hashpw(user_password, user.password_hash) != user.password_hash:
            return

        kwargs.pop('user_password')
        return func(**kwargs)

    wrapper.__name__ = func.__name__
    return wrapper
