FROM python:2.7.10-onbuild
MAINTAINER Amo Chen <spitfire.sidra@gmail.com>
RUN adduser --disabled-password --gecos '' worker \
    && pip install -r requirements.txt \
    && cat "RABBITMQ_PORT_5672_TCP_ADDR=$RABBITMQ_PORT_5672_TCP_ADDR" >> /etc/profile \
    && cat "RABBITMQ_PORT_5672_TCP_PORT=$RABBITMQ_PORT_5672_TCP_PORT" >> /etc/profile \
    && su -m worker -c "celery worker -A tasks.TASK_QUEUE --loglevel=info --concurrency=1"
EXPOSE 4567
ENTRYPOINT python webhookapp.py
