#!/usr/bin/env bash

cd /usr/share/webapps/chamados

exec /usr/share/envs/chamados/bin/gunicorn config.wsgi -c deploy/staging/gunicorn.conf.py  --env DJANGO_SETTINGS_MODULE=config.settings.production
