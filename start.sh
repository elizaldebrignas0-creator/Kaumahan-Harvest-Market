#!/bin/bash
echo "Running migrations..."
python manage.py migrate
echo "Creating admin user..."
python create_test_admin.py
echo "Starting server..."
gunicorn kaumahan.wsgi:application --bind 0.0.0.0:$PORT