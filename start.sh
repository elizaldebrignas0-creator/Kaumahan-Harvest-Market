#!/bin/bash
echo "Running migrations with PostgreSQL..."
python manage.py migrate --settings=kaumahan.production_settings
echo "Creating admin user if needed..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.production_settings')
import django
django.setup()
from marketplace.models import CustomUser
if not CustomUser.objects.filter(email='pelaezelizalde0@gmail.com').exists():
    CustomUser.objects.create_superuser(
        email='pelaezelizalde0@gmail.com',
        password='admin123',
        full_name='Admin User',
        phone_number='09123456789',
        address='Admin Address'
    )
    print('✅ Admin user created')
else:
    print('✅ Admin user already exists')
"
echo "Starting server with PostgreSQL..."
gunicorn kaumahan.wsgi:application --bind 0.0.0.0:$PORT