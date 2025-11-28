from .settings_cloudinary import *
import os

DEBUG = False
ALLOWED_HOSTS = ['*']
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key-12345')

# PostgreSQL Database - Ensure PostgreSQL is used in production
import dj_database_url

# First try DATABASE_URL from environment
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
    print(f"✅ Using PostgreSQL from DATABASE_URL: {os.environ.get('DATABASE_URL')}")
else:
    # Fallback to SQLite ONLY if no DATABASE_URL provided
    DATABASES = {
        'default': dj_database_url.config(
            default='sqlite:///db.sqlite3',
            conn_max_age=600
        )
    }
    print("⚠️ WARNING: No DATABASE_URL found, using SQLite fallback")

# Ensure we're not accidentally using SQLite in production
if DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    print("🚨 CRITICAL: Using SQLite in production! Data will be lost!")
else:
    print("✅ PostgreSQL database configured correctly")

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True