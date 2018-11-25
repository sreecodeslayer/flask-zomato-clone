from foogg.app import create_app
from foogg.models import Users
from foogg.extensions import pwd_context
create_app()
# create a default manager
mng = Users(username='john', roles=['manager'], email='john@foog.co')
mng.passwd_digest = pwd_context.hash('john')
mng.save()

# create a default valet
val = Users(username='kevin', roles=['valet'], email='kevin@foog.co')
val.passwd_digest = pwd_context.hash('kevin')
val.save()
