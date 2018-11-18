from datetime import datetime, timedelta
from foogg.extensions import ma
from .user import UserSchema
from .base import ObjectId
from ..models import Jobs, History

from marshmallow.exceptions import ValidationError
from marshmallow import post_load

PRIORITIES = ['low', 'medium', 'high']


def validate_choice(value):
    if value in PRIORITIES:
        return True
    else:
        raise ValidationError(
            f'Priority can be any of {PRIORITIES}')


class HistorySchema(ma.Schema):

    id = ObjectId(dump_only=True)
    status = ma.String(dump_only=True)
    made_at = ma.DateTime(dump_only=True)
    taken_at = ma.DateTime(dump_only=True)

    @post_load
    def make_history(self, data):
        return Histroy(**data)


class JobSchema(ma.Schema):
    id = ObjectId(dump_only=True)
    title = ma.String(required=True)
    status = ma.String(dump_only=True)
    priority = ma.String(required=True, validate=validate_choice)
    created_on = ma.DateTime(default=datetime.utcnow)
    created_by = ma.Nested(UserSchema)
    history = ma.List(ma.Nested(HistorySchema))

    @post_load
    def make_job(self, data):
        return Jobs(**data)
