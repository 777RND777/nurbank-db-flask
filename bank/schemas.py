from marshmallow import Schema, validate
from marshmallow.fields import Boolean, Integer, String


class UserSchema(Schema):
    pk = Integer(dump_only=True)
    id = Integer()
    first_name = String(validate=[validate.Length(max=250)])
    last_name = String(validate=[validate.Length(max=250)])
    username = String(validate=[validate.Length(max=250)])
    nickname = String(validate=[validate.Length(max=250)])
    debt = Integer()


class ApplicationSchema(Schema):
    pk = Integer(dump_only=True)
    id = Integer()
    value = Integer()
    request_date = String(validate=[validate.Length(max=50)])
    answer_date = String(validate=[validate.Length(max=50)])
    approved = Boolean()
    is_admin = Boolean()

    user_id = Integer()
