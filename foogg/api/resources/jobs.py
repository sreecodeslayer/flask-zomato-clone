from .base import ManagerResources, JWTResource, DeliveryValetResources
from ...schemas import JobSchema, PRIORITIES
from ...models import Jobs, History
from ...helpers import paginate
from ...extensions import rmq, socketio
from ...log import logger
from flask import request, jsonify, make_response
from flask_jwt_extended import get_current_user
from datetime import datetime


ALLOWEDSTATUS = ['accepted', 'declined', 'completed', 'cancelled']


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
        rmq.publish_job(queue_string, PRIORITIES.get(job.priority))
        # Send the notification as it need not wait for the beat

        socketio.emit(
            'realtime',
            {
                'message': 'A new task is available',
                'status': True
            },
            json=True,
            room='realtime_updates',
            namespace='/updates'
        )
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


class ValetDeliveriesResource(DeliveryValetResources):
    def get(self):
        schema = JobSchema(many=True)
        previous = ['accepted', 'completed', 'declined', 'cancelled']
        jobs = Jobs.objects(
            valet=get_current_user(), status__in=previous)
        by_status = request.args.get('status')
        if by_status:
            jobs = jobs.filter(status=by_status)
        return paginate(jobs, schema)


class JobStatusResource(JWTResource):

    def patch(self, jid):
        if not request.is_json:
            return make_response(
                jsonify(message='Missing JSON in request'), 400)
        schema = JobSchema(partial=True)
        job = Jobs.objects.get_or_404(id=jid)
        status = request.json.get('status')
        if status not in ALLOWEDSTATUS:
            return make_response(
                jsonify(
                    message='Invalid status, aborting status updation,'
                    ' allowed states inlcude %s' % (ALLOWEDSTATUS)
                ), 400
            )
        curr_user = get_current_user()
        if job.status == status or job.status == 'cancelled':
            return make_response(
                jsonify(message=f'Job already {job.status}'),
                422
            )
        if status == 'cancelled':
            # verify user is a manager
            if not curr_user.is_manager:
                return make_response(
                    jsonify(message='Not authorized to cancel jobs'),
                    401
                )
        if curr_user.is_valet:
            valet = curr_user
            if status == 'declined':
                valet = None
                queue_string = str(job.id)
                # Insert it back into queue
                rmq.publish_job(queue_string, PRIORITIES.get(job.priority))

        change = f'{job.status}=>{status}'
        job.update(valet=valet)
        job.update(status=status)
        job.update(add_to_set__history=[History(
            status=status, made_at=datetime.utcnow)])

        msg = f'{curr_user.username} updated job [{job.title}]'
        socketio.emit(
            'realtime-manager',
            {
                'message': msg,
                'change': change,
                'status': True
            },
            json=True,
            room='realtime-manager-updates',
            namespace='/updates'
        )

        return schema.jsonify(job.reload())


class ValetJobResource(DeliveryValetResources):
    def get(self):

        # Check if valet has more than 3 pending jobs
        curr_user = get_current_user()
        jobs = Jobs.objects(
            valet=curr_user, status__in=['accepted']).count()
        logger.debug(f'User has {jobs} tasks in accepted state')
        if jobs > 2:
            return make_response(
                jsonify(
                    message=f'You have currently {jobs} jobs pending.'
                    ' Please complete them'
                ), 422)
        jid = rmq.seek_job()
        job = Jobs.objects.get_or_404(id=jid)
        if job.status != 'cancelled':
            schema = JobSchema()
            return schema.jsonify(job)
        else:
            make_response(
                jsonify(message='Job has been cancelled by manager'),
                422
            )
