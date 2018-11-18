from .base import ManagerResources
from ...schemas import JobSchema
from ...models import Jobs
from ...helpers import paginate


class JobsResource(ManagerResources):
    def get(self):
        schema = JobSchema(many=True)
        jobs = Jobs.objects()
        return paginate(jobs, schema)


class JobResource(ManagerResources):
    def get(self, jid):
        pass
