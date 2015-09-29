#! /bin/bash

set -x
chown worker:worker workspace
su -m worker -c "celery worker -A tasks.TASK_QUEUE --loglevel=info --concurrency=1"
