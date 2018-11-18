from ..log import logger
from functools import wraps
from flask_jwt_extended import get_current_user, verify_jwt_in_request
from flask import jsonify, make_response


def is_manager(fn):
    '''
    Here is a custom decorator that verifies the JWT is present in the request,
    as well as insuring that this user is a manager.
    '''
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = get_current_user()
        logger.debug('User roles => %s' % user.roles)
        if 'manager' not in set(user.roles):
            return make_response(
                jsonify(
                    message='You have to be a manager to be here'
                ), 403
            )
        else:
            return fn(*args, **kwargs)
    return wrapper


def is_delivery_valet(fn):
    '''
    Here is a custom decorator that verifies the JWT is present in the request,
    as well as insuring that this user is a delivery guy.
    '''
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = get_current_user()
        logger.debug('User roles => %s' % user.roles)
        if 'valet' not in set(user.roles):
            return make_response(
                jsonify(
                    message='You have to be a delivery valet to be here'
                ), 403
            )
        else:
            return fn(*args, **kwargs)
    return wrapper
