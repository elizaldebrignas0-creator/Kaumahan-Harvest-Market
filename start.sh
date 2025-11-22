#!/bin/bash
python manage.py migrate
gunicorn kaumahan.wsgi:application --bind 0.0.0.0:$PORT