FROM debian:buster-slim

LABEL maintainer="Rémi Duraffort <remi.duraffort@linaro.org>"

ENV DEBIAN_FRONTEND noninteractive

RUN echo 'deb http://deb.debian.org/debian buster-backports main' > /etc/apt/sources.list.d/backports.list && \
    mkdir -p /usr/share/man/man1 /usr/share/man/man7 && \
    groupadd --system --gid 200 lavaserver && \
    useradd --system --home /var/lib/lava-server/home/ --uid 200 --gid 200 --shell /bin/sh lavaserver && \
    apt-get update -q && \
    apt-get install --no-install-recommends --yes apache2 gunicorn3 postgresql postgresql-client postgresql-common python3-setuptools && \
    apt-get install --no-install-recommends --yes python3-voluptuous python3-yaml python3-zmq && \
    apt-get install --no-install-recommends --yes python3-django python3-django-auth-ldap python3-django-filters python3-django-tables2 python3-djangorestframework python3-djangorestframework-extensions python3-djangorestframework-filters python3-docutils python3-jinja2 python3-junit.xml python3-psycopg2 python3-requests python3-simplejson python3-tap python3-tz python3-voluptuous python3-whitenoise python3-yaml python3-zmq && \
    apt-get install --no-install-recommends --yes python3-pip && \
    python3 -m pip install sentry-sdk==0.14.1 && \
    rm -rf /var/lib/apt/lists/*
