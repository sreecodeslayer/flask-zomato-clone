from flask_restful import Resource
from flask_jwt_extended import jwt_required
from ...helpers.permissions import is_manager, is_delivery_valet


class JWTResource(Resource):
    method_decorators = [jwt_required]


class ManagerResources(Resource):
    method_decorators = [jwt_required, is_manager]


class DeliveryValetResources(Resource):
    method_decorators = [jwt_required, is_delivery_valet]
