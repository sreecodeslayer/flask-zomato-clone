from datetime import datetime, timedelta
from foogg.extensions import ma
from .user import UserSchema
from marshmallow.exceptions import ValidationError
PRIORITIES = {
    0: 'LOW',
    1: 'MEDIUM',
    2: 'HIGH'
}


def validate_choice(value):
    if value in PRIORITIES.values():
        return True
    else:
        raise ValidationError(f'Priority can be any of {PRIORITIES.values()}')


class JobSchema(ma.Schema):
    title = ma.String(required=True)
    priority = ma.String(required=True, validate=validate_choice)
    created_on = ma.DateTime(default=datetime.utcnow)
    created_by = ma.Nested(UserSchema)
