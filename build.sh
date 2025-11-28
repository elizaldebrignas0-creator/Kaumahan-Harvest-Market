#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Set up media directories for persistent storage
python manage.py setup_media_directories

echo "Build completed - media directories ready"
echo "Media root: ${MEDIA_ROOT:-/opt/render/project/src/media}"
ls -la ${MEDIA_ROOT:-/opt/render/project/src/media}/ || echo "Media directory not yet created"