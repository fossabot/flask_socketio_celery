from datetime import datetime
from random import randint
from apps.celery.factory import create_celery_app

from apps.extensions import socketio

celery = create_celery_app()
realtime_chart_data = []


@celery.task(name='add_together')
def add_together(a, b):
    return a + b


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        2.0,
        realtime_chart.s(),
        name='send realtime_chart every 2 seconds')


@celery.task(name='realtime_chart')
def realtime_chart():
    datetime_now = datetime.now()
    date = datetime_now.strftime("%Y-%m-%d %H:%M:%S")
    random_value = randint(0, 20)
    data_item = {"date": date, "value": random_value}
    realtime_chart_data.append(data_item)
    socketio.emit('realtime_chart', realtime_chart_data)
    return True
