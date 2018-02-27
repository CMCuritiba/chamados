#!/usr/bin/env bash

cd /usr/share/webapps/chamados

mkdir -p /usr/share/webapps/chamados/var/run
rm -f /usr/share/webapps/chamados/var/run/*

exec /usr/share/envs/chamados/bin/gunicorn config.wsgi -c deploy/staging/gunicorn.conf.py  --env DJANGO_SETTINGS_MODULE=config.settings.production
