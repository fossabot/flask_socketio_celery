import logging
from flask import Blueprint, render_template, request
from flask_login import login_required
from flask_socketio import send, emit, join_room
from apps.extensions import login_manager, socketio
from apps.auth.models import User


logger = logging.getLogger('socketio')
blueprint = Blueprint('socketio', __name__, url_prefix='/socketio')


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@blueprint.route('/index/', methods=['GET'])
@login_required
def index():
    return render_template('socketio_example/index.html')


@socketio.on('connect')
def test_connect():
    logger.info(request.sid + ' Connected')
    emit('message', {'data': request.sid + ' Connected'})


@socketio.on('user_bind_sid')
def user_bind_sid(message):
    """
        绑定 user 和 sid
    """
    user_id = message['user_id']
    sid = message['sid']
    user = User.get_by_id(user_id)
    user.sid = sid
    user.save()


@socketio.on('join')
def on_join(message):
    room = message['user_id']
    join_room(room)
    send(room + ' has entered the room.', room=room)


@socketio.on('message')
def handle_message(message):
    emit('message', message)


@socketio.on('admin_notify_receive')
def admin_notify_receive(message):
    """
        发送通知
    """
    if message:
        socketio.emit('admin_notify', message)
