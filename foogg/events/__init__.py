from flask_socketio import emit, join_room, leave_room, disconnect
from ..extensions import socketio, rmq
from ..log import logger
from threading import Lock
from flask import request
from flask_jwt_extended import jwt_required
from flask_socketio import join_room, leave_room, emit, send
from threading import Lock

ROOM = 'realtime_updates'

thread = None
lock = Lock()


def background_thread():
    """Check if the queue is empty here, send broadcast if not"""
    count = 0
    while True:
        socketio.sleep(15)
        count = rmq.count
        logger.debug(f'{count} tasks are in queue')
        if count:
            socketio.emit(
                'realtime',
                {
                    'message': 'A new task is available'
                },
                json=True,
                namespace='/updates'
            )


with lock:
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)


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
