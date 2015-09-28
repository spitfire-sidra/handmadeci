# -*- coding: utf-8 -*-
from celery import Celery

import config


def get_task_queue():

    if config.IRONMQ is True:
        task_queue = Celery(
            broker=config.IRONMQ_BROKER_URL,
            backend=config.IRONMQ_CACHE_BACKEND
        )
    else:
        task_queue = Celery(broker=config.RABBITMQ_BROKER_URL)

    return task_queue
