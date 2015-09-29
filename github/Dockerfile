FROM python:2.7.10-onbuild
MAINTAINER Amo Chen <spitfire.sidra@gmail.com>
RUN set -x \
    && adduser --disabled-password --gecos '' worker \
    && pip install -r requirements.txt
