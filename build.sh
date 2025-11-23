#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Set up media files for production
python setup_media.py

echo "Build completed - media files ready"
ls -la media/products/ | head -5