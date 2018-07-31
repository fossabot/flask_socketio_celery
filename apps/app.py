import os
import logging
import eventlet    # use celery with socketio need some monkey_patch
from flask import Flask, render_template
from apps.extensions import (bcrypt, cache, csrf_protect, db,
                             login_manager, migrate, socketio)
from apps.settings import ProdConfig
from apps import commands, public, auth, socketio_example


eventlet.monkey_patch()    # use celery with socketio need some monkey_patch


def create_app(config_object=ProdConfig):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    register_socketio_logger(config_object)
    return app


def register_extensions(app):
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(
        app, async_mode='eventlet', message_queue=app.config['REDIS_URL'])
    return None


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(socketio_example.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('partials/{0}.html'.format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': auth.models.User,
            'Role': auth.models.Role,
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)


def register_socketio_logger(config):
    logger = logging.getLogger('socketio')
    logger.setLevel(logging.INFO)
    fmter = logging.Formatter(
        '%(levelname)s %(asctime)s %(module)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    hdlr = logging.FileHandler(
        os.path.join(config.PROJECT_ROOT, 'logs', 'socketio.log'))
    hdlr.setFormatter(fmt=fmter)
    logger.addHandler(hdlr=hdlr)
