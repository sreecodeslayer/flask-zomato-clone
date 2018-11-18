from .base import ManagerResources, JWTResource
from ...schemas import JobSchema
from ...models import Jobs, History
from ...helpers import paginate
from ...log import logger
from flask import request, jsonify, make_response
from flask_jwt_extended import get_current_user
from datetime import datetime


class JobsResource(ManagerResources):
    def get(self):
        schema = JobSchema(many=True)
        jobs = Jobs.objects()
        return paginate(jobs, schema)

    def post(self):
        if not request.is_json:
            return make_response(
                jsonify(message='Missing JSON in request'), 400)
        schema = JobSchema()
        job, errors = schema.load(request.json)
        if errors:
            return make_response(
                jsonify(errors=errors), 422
            )
        job.history.append(History())
        job.created_by = get_current_user()
        job.save()
        queue_string = str(job.id)
        # Insert it into queue

        # Publish to websocket room

        return schema.jsonify(job)


class JobResource(ManagerResources):
    def get(self, jid):
        schema = JobSchema()
        job = Jobs.objects.get_or_404(id=jid)
        return schema.jsonify(job)

    def delete(self, jid):
        job = Jobs.objects.get_or_404(id=jid)
        job.delete()
        return jsonify(message='Job removed')


class JobStatusResource(JWTResource):

    ALLOWEDSTATUS = ['accepted', 'declined', 'completed', 'cancelled']

    def patch(self, jid):
        if not request.is_json:
            return make_response(
                jsonify(message='Missing JSON in request'), 400)
        schema = JobSchema(partial=True)
        job = Jobs.objects.get_or_404(id=jid)
        status = request.json.get('status')
        if status not in self.ALLOWEDSTATUS:
            return make_response(
                jsonify(
                    message='Invalid status, aborting status updation,'
                    ' allowed states inlcude %s' % (self.ALLOWEDSTATUS)
                ), 400
            )

        # get prioratised job here
        job.update(status=status)
        job.update(add_to_set__history=[History(
            status=status, made_at=datetime.utcnow)])

        return schema.jsonify(job.reload())
