from flask.helpers import get_debug_flag
from apps.settings import DevConfig, ProdConfig
from apps.app import create_app
from celery import Celery


def create_celery_app(app=None):
    CONFIG = DevConfig if get_debug_flag() else ProdConfig
    app = app or create_app(CONFIG)
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
