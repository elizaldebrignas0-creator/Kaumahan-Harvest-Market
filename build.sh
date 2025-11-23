#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# Set up media files for production
python setup_media.py

# Ensure static products directory exists
mkdir -p static/products

# Copy any product images to static directory
if [ -d "media/products" ]; then
    cp -r media/products/* static/products/ 2>/dev/null || true
fi

echo "Build completed with media and static files"
ls -la static/products/ | head -5