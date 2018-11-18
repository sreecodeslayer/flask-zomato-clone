from .base import ManagerResources


class JobsResource(ManagerResources):
    def get(self):
        pass


class JobResource(ManagerResources):
    def get(self, jid):
        pass
