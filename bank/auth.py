from bank.models import User


def check_user(func):
    def wrapper(**kwargs):
        pass_key = 'user_id' if 'user_id' in kwargs.keys() else 'id'
        user = User.get(kwargs[pass_key])
        if not user or user.password_hash != kwargs['user_password']:
            return
        kwargs.pop('user_password')
        return func(**kwargs)

    wrapper.__name__ = func.__name__
    return wrapper
