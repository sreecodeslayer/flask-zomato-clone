from marshmallow import (
    fields,
    validate,
    post_load
)

from foogg.extensions import ma
from foogg.models import Users
from .base import ObjectId


class UserSchema(ma.Schema):
    id = ObjectId(dump_only=True)
    username = ma.String(required=True)
    email = ma.String(
        required=True,
        validate=validate.Email(
            error='Not a valid email address')
    )
    passwd_digest = ma.String(load_only=True, required=True)
    roles = ma.List(ma.String, default=['manager'])
    joined_on = ma.DateTime(dump_only=True)

    @post_load
    def make_user(self, data):
        return Users(**data)
