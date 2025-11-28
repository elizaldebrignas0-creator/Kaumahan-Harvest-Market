#!/bin/bash
echo "Running migrations..."
python manage.py migrate --settings=kaumahan.settings_build
echo "Making user admin..."
python create_admin_simple.py
echo "Admin script completed"
echo "Starting server..."
gunicorn kaumahan.wsgi:application --bind 0.0.0.0:$PORT