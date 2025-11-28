from .settings_cloudinary import *
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

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True