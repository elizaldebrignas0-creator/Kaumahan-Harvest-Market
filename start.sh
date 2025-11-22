#!/bin/bash
export DJANGO_SETTINGS_MODULE=kaumahan.production_settings
python manage.py migrate
gunicorn kaumahan.wsgi:application --bind 0.0.0.0:8000