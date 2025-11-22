#!/bin/bash
echo "Running migrations..."
python manage.py migrate
echo "Creating new admin..."
python create_new_admin.py
echo "Starting server..."
gunicorn kaumahan.wsgi:application --bind 0.0.0.0:$PORT