#!/bin/bash
echo "Setting up PostgreSQL database..."
python setup_postgresql.py
echo "Starting server with PostgreSQL..."
gunicorn kaumahan.wsgi:application --bind 0.0.0.0:$PORT