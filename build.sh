#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Ensure media directory exists for production
mkdir -p media
mkdir -p media/products

echo "Build completed - media directory ready"
ls -la media/ 2>/dev/null || echo "No media directory found"