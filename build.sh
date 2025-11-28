#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

echo "Build completed - S3 media storage configured"
echo "Environment: ${DEBUG:-False}"
echo "Storage backend: ${DEFAULT_FILE_STORAGE:-Default}"