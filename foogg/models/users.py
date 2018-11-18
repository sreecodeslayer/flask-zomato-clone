from foogg.extensions import db, pwd_context
from datetime import datetime, timedelta


class Users(db.Document):
    '''Mongodb Model for Users'''
    username = db.StringField(required=True, unique=True)
    email = db.EmailField(unique=True)
    passwd_digest = db.StringField()
    roles = db.ListField(default=['manager'])
    joined_on = db.DateTimeField(default=datetime.utcnow)

    meta = {
        'indexes': ['username', 'email', 'joined_on']
    }

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)

    def __repr__(self):
        return '(User : %s)' % self.username
