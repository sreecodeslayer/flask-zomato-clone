from flask_socketio import emit, join_room, leave_room, disconnect
from ..extensions import socketio
from ..log import logger
from threading import Lock
from flask import request
from flask_jwt_extended import jwt_required
from flask_socketio import join_room, leave_room, emit, send
ROOM = 'realtime_updates'


@socketio.on('connect', namespace='/updates')
def connected():
    logger.debug('Client [%s] connected for updates' % (request.sid))
    join_room(ROOM)
    emit(
        'status', {'title': 'Welcome!',
                   'message': 'You are now connected to real time updates'},
        room=ROOM,
        json=True,
        namespace='/updates'
    )


@socketio.on('disconnect', namespace='/updates')
def disconnect():
    logger.debug('Client [%s] disconnected from updates' % (request.sid))
    leave_room(ROOM)
