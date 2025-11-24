from .settings import *
import os

DEBUG = False
ALLOWED_HOSTS = ['*']
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-12345')

# PostgreSQL Database
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Production Media Configuration
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '/opt/render/project/src/media')

# Ensure media directory exists
import django
from django.conf import settings
if not settings.DEBUG:
    import os
    os.makedirs(MEDIA_ROOT, exist_ok=True)
    os.makedirs(os.path.join(MEDIA_ROOT, 'products'), exist_ok=True)
    os.makedirs(os.path.join(MEDIA_ROOT, 'business_permits'), exist_ok=True)

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True