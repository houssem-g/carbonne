from __future__ import absolute_import
from celery import Celery
import os


REDIS_BROKER_URL = os.getenv('REDIS_BROKER_URL', 'redis://localhost:6379/0')
REDIS_BACKEND_URL = os.getenv('REDIS_BACKEND_URL', 'redis://localhost:6379/0')


def make_celery():

    celery_app = Celery(
        'celery_config',
        broker=REDIS_BROKER_URL,
        backend=REDIS_BACKEND_URL,
        broker_connection_retry_on_startup=True,
        task_track_started=True,
        worker_send_task_events=True,
        result_expires=3600,
    )

    celery_app.conf.update(
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='UTC',
        enable_utc=True,
    )

    CELERY_CONFIG = {
        'CELERYD_ENV_OPTS': {
            'PYTHONPATH': '/app',
        }
    }

    celery_app.conf.update(CELERY_CONFIG)
    celery_app.autodiscover_tasks(["app.tasks.multiply", "app.tasks.periodic_tasks"])

    return celery_app


celery_app = make_celery()
