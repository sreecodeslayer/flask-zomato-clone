from .base import ManagerResources
from ...schemas import JobSchema
from ...models import Jobs
from ...helpers import paginate
from flask import request, jsonify, make_response
from flask_jwt_extended import get_current_user


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
        job.created_by = get_current_user()
        job.save()
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
