from datetime import datetime, timedelta
from foogg.extensions import db
from .users import Users

PRIORITIES = {
    0: 'LOW',
    1: 'MEDIUM',
    2: 'HIGH'
}


class Jobs(db.Document):
    title = db.StringField(max_length=75, required=True)
    priority = db.StringField(max_length=6, required=True)
    created_on = db.DateTimeField(default=datetime.utcnow)
    created_by = db.ReferenceField(Users)

    meta = {
        'indexes': ['priority', 'created_on']
    }
