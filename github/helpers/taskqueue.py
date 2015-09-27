# -*- coding: utf-8 -*-
from celery import Celery

from github import config


def get_task_queue():

    if config.IRONMQ is True:
        celery = Celery(broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)
    else:
        celery = Celery(broker=RABBITMQ_BROKER_URL)

    return celery
