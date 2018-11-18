from datetime import datetime, timedelta
from foogg.extensions import ma
from .user import UserSchema
from .base import ObjectId
from ..models import Jobs

from marshmallow.exceptions import ValidationError
from marshmallow import post_load

PRIORITIES = ['low', 'medium', 'high']


def validate_choice(value):
    if value in PRIORITIES:
        return True
    else:
        raise ValidationError(
            f'Priority can be any of {PRIORITIES}')


class JobSchema(ma.Schema):
    id = ObjectId()
    title = ma.String(required=True)
    priority = ma.String(required=True, validate=validate_choice)
    created_on = ma.DateTime(default=datetime.utcnow)
    created_by = ma.Nested(UserSchema)

    @post_load
    def make_job(self, data):
        return Jobs(**data)
