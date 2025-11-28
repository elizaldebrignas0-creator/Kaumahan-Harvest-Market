"""
Alternative settings for Cloudinary storage
Replace the media configuration in settings.py with this if you choose Cloudinary
"""

# Media files configuration - Cloudinary
MEDIA_URL = "/media/"

# Development: Local media storage
if DEBUG:
    MEDIA_ROOT = BASE_DIR / "media"
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
else:
    # Production: Cloudinary Storage
    MEDIA_ROOT = ''  # Not used with Cloudinary
    DEFAULT_FILE_STORAGE = 'kaumahan.cloudinary_storage.CloudinaryStorage'
    
    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET')
    
    # Media URL configuration (Cloudinary URLs)
    MEDIA_URL = f'https://res.cloudinary.com/{CLOUDINARY_CLOUD_NAME}/image/upload/'
    
    # Static files configuration (keep using whitenoise)
    STATIC_URL = "/static/"
    STATICFILES_DIRS = [BASE_DIR / "static"]
    STATIC_ROOT = BASE_DIR / "staticfiles"
