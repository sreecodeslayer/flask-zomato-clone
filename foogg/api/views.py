from flask import Blueprint
from flask_restful import Api

from foogg.api.resources import (
    UserResource,
    UsersResource,
    JobsResource,
    JobResource
)


blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(UserResource, '/users/<uid>')
api.add_resource(UsersResource, '/users')

api.add_resource(JobResource, '/jobs/<jid>')
api.add_resource(JobsResource, '/jobs')
