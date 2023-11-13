#!/bin/sh
python manage.py migrate
gunicorn config.wsgi -b 0.0.0.0:8000 --chdir=/usr/src/api
