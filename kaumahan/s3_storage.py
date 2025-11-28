"""
AWS S3 Storage Configuration for Django
Handles both development and production environments
"""

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import safe_join


class MediaStorage(S3Boto3Storage):
    """
    Custom S3 storage for media files
    """
    def __init__(self, *args, **kwargs):
        # Override settings for production
        if not settings.DEBUG:
            # Production settings
            self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            self.custom_domain = f'{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
            self.file_overwrite = False
            self.default_acl = 'public-read'
            self.querystring_auth = False
            self.access_key = settings.AWS_ACCESS_KEY_ID
            self.secret_key = settings.AWS_SECRET_ACCESS_KEY
            self.region_name = settings.AWS_S3_REGION_NAME
            self.secure_urls = settings.AWS_S3_SECURE_URLS
            self.endpoint_url = settings.AWS_S3_ENDPOINT_URL
            
        super().__init__(*args, **kwargs)

    def get_valid_name(self, name):
        """
        Generate valid filename for S3
        """
        # Ensure name starts with media prefix
        if not name.startswith('media/'):
            name = safe_join('media', name)
        return name

    def url(self, name):
        """
        Generate URL for the file
        """
        # Remove media/ prefix for clean URLs
        if name.startswith('media/'):
            name = name[6:]  # Remove 'media/' prefix
        
        if not settings.DEBUG:
            # Production: Use S3 URL
            return f"https://{self.custom_domain}/{name}"
        else:
            # Development: Use local URL
            return f"{settings.MEDIA_URL}{name}"


class StaticStorage(S3Boto3Storage):
    """
    S3 storage for static files (optional)
    """
    location = 'static'
    default_acl = 'public-read'
