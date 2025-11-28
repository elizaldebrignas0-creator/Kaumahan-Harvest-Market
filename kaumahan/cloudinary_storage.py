"""
Cloudinary Storage Configuration for Django
Easy setup with automatic optimization and transformations
"""

from django.conf import settings
from storages.backends.cloudinary_storage import CloudinaryStorage


class MediaCloudinaryStorage(CloudinaryStorage):
    """
    Custom Cloudinary storage for media files
    """
    def __init__(self, *args, **kwargs):
        # Configure Cloudinary settings
        if not settings.DEBUG:
            self.cloud_name = settings.CLOUDINARY_CLOUD_NAME
            self.api_key = settings.CLOUDINARY_API_KEY
            self.api_secret = settings.CLOUDINARY_API_SECRET
            
        super().__init__(*args, **kwargs)

    def url(self, name):
        """
        Generate optimized Cloudinary URL
        """
        if not settings.DEBUG:
            # Production: Use Cloudinary URL with optimizations
            base_url = super().url(name)
            
            # Add automatic optimizations for images
            if name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                # Auto-optimize: quality, format, and responsive
                optimizations = 'q_auto,f_auto,w_auto,h_auto,c_scale'
                return f"{base_url}?{optimizations}"
            
            return base_url
        else:
            # Development: Use local URL
            return f"{settings.MEDIA_URL}{name}"

    def get_valid_name(self, name):
        """
        Generate valid filename for Cloudinary
        """
        # Organize files in folders
        if name.startswith('products/'):
            return name  # Already organized
        else:
            return f"products/{name}"


class StaticCloudinaryStorage(CloudinaryStorage):
    """
    Cloudinary storage for static files (optional)
    """
    def __init__(self, *args, **kwargs):
        # Static files don't need optimizations
        super().__init__(*args, **kwargs)
