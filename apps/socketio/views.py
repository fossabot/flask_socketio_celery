from flask import Blueprint, render_template
from flask_login import login_required

from apps.extensions import login_manager
from apps.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/socketio')


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))


@blueprint.route('/example/', methods=['GET'])
@login_required
def example():
    return render_template('socketio/example.html')
