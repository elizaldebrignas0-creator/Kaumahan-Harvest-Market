#!/bin/bash
python manage.py migrate
python manage.py create_admin
gunicorn kaumahan.wsgi:application --bind 0.0.0.0:$PORT