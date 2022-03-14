from marshmallow import Schema, validate
from marshmallow.fields import Boolean, Integer, String


class ApplicationSchemaBase(Schema):
    id = Integer()
    user_id = Integer(required=True)
    password = String(required=True, validate=[validate.Length(max=250)])


class ApplicationSchemaCreate(ApplicationSchemaBase):
    value = Integer(required=True)
    request_date = String(required=True, validate=[validate.Length(max=50)])
    is_admin = Boolean()


class ApplicationSchemaApprove(ApplicationSchemaBase):
    answer_date = String(required=True, validate=[validate.Length(max=50)])
    approved = Boolean(required=True)


class ApplicationSchema(ApplicationSchemaBase):
    pk = Integer(dump_only=True)
    value = Integer()
    request_date = String(validate=[validate.Length(max=50)])
    answer_date = String(validate=[validate.Length(max=50)])
    approved = Boolean()
    is_admin = Boolean()


class UserSchemaBase(Schema):
    id = Integer()
    password = String(required=True, validate=[validate.Length(max=250)])


class UserSchemaCreate(UserSchemaBase):
    first_name = String(required=True, validate=[validate.Length(max=250)])
    last_name = String(required=True, validate=[validate.Length(max=250)])
    username = String(required=True, validate=[validate.Length(max=250)])


class UserSchema(UserSchemaBase):
    pk = Integer(dump_only=True)
    first_name = String(validate=[validate.Length(max=250)])
    last_name = String(validate=[validate.Length(max=250)])
    username = String(validate=[validate.Length(max=250)])
    nickname = String(validate=[validate.Length(max=250)])
    debt = Integer()
