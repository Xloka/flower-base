import os
import time
from datetime import datetime

from celery import Celery
from celery.schedules import crontab


app = Celery(
    "tasks",
    broker=os.environ.get("CELERY_BROKER_URL", "redis://"),
    backend=os.environ.get("CELERY_RESULT_BACKEND", "redis"),
)
app.conf.CELERY_ACCEPT_CONTENT = ["pickle", "json", "msgpack", "yaml"]
app.conf.CELERY_WORKER_SEND_TASK_EVENTS = True
app.config_from_object("celeryconfig")

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(100, echo.s('hey loka'))


@app.task
def add(x, y):
    return x + y


@app.task
def sleep(seconds):
    time.sleep(seconds)


@app.task
def echo(msg, timestamp=False):
    return "%s: %s" % (datetime.now(), msg) if timestamp else msg


@app.task
def error(msg):
    raise Exception(msg)


if __name__ == "__main__":
    app.start()
