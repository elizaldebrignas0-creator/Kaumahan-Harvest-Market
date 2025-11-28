#!/bin/bash
echo "Running migrations..."
python manage.py migrate --settings=kaumahan.settings_build --fake
echo "Force creating database and admin..."
python force_setup.py
echo "Starting server..."
gunicorn kaumahan.wsgi:application --bind 0.0.0.0:$PORT