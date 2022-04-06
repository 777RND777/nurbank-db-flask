from datetime import datetime
from random import randint

from bank.models import Application


def get_current_time() -> str:
    return datetime.now().strftime("%H:%M:%S - %d/%m/%Y")


def get_unique_id():
    _id = randint(100000000, 999999999)
    while Application.get(_id):
        _id = randint(100000000, 999999999)
    return _id
