from apps.celery.factory import create_celery_app

from apps.extensions import socketio
# from apps.socketio.models import Company

celery = create_celery_app()


@celery.task(name='add_together')
def add_together(a, b):
    return a + b


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        30.0,
        socketio_example.s(),
        name='send socketio_example every 30 seconds')


@celery.task(name='socketio_example')
def socketio_example():
    pass
    # socketio.emit('socketio_example', company.to_json())
    # return True
