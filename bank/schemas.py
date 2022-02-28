from marshmallow import Schema, validate
from marshmallow.fields import Boolean, Integer, Nested, String


class ApplicationSchema(Schema):
    pk = Integer(dump_only=True)
    id = Integer()
    value = Integer()
    request_date = String(validate=[validate.Length(max=50)])
    answer_date = String(validate=[validate.Length(max=50)])
    approved = Boolean()
    is_admin = Boolean()

    user_id = Integer()


class UserSchemaBase(Schema):
    id = Integer()
    first_name = String(validate=[validate.Length(max=250)])
    last_name = String(validate=[validate.Length(max=250)])
    username = String(validate=[validate.Length(max=250)])
    nickname = String(validate=[validate.Length(max=250)])


class UserSchemaCreate(UserSchemaBase):
    pass


class UserSchema(UserSchemaBase):
    pk = Integer(dump_only=True)
    debt = Integer()

    applications = Nested(ApplicationSchema, many=True, dump_only=True)
