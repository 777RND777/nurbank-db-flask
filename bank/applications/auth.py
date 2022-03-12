from bank.models import User


def check_user(func):
    def wrapper(**kwargs):
        user = User.get(kwargs['user_id'])
        if not user or user.password_hash != kwargs['user_password']:
            return
        kwargs.pop('user_password')
        return func(**kwargs)

    wrapper.__name__ = func.__name__
    return wrapper
