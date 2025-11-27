"""
Custom storage backend for Render Persistent Disk
Ensures persistent media file storage in production
"""

import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class RenderPersistentStorage(FileSystemStorage):
    """
    Custom storage backend for Render's persistent disk.
    Handles both development and production environments.
    """
    
    def __init__(self, **kwargs):
        # Ensure media directory exists
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        
        super().__init__(location=settings.MEDIA_ROOT, **kwargs)
    
    def save(self, name, content, max_length=None):
        """
        Save the file and ensure proper directory structure
        """
        # Create directory if it doesn't exist
        full_path = os.path.join(settings.MEDIA_ROOT, name)
        directory = os.path.dirname(full_path)
        
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        # Call parent save method
        return super().save(name, content, max_length)
    
    def url(self, name):
        """
        Return the URL to access the file
        """
        if settings.DEBUG:
            # Development: use Django's media serving
            return f"{settings.MEDIA_URL}{name}"
        else:
            # Production: ensure proper media URL
            return f"{settings.MEDIA_URL}{name}"
    
    def exists(self, name):
        """
        Check if file exists
        """
        return super().exists(name)
    
    def delete(self, name):
        """
        Delete the file
        """
        return super().delete(name)


# Production-specific storage for Render
class RenderProductionStorage(RenderPersistentStorage):
    """
    Production storage with additional safety checks
    """
    
    def __init__(self, **kwargs):
        # Verify persistent disk is mounted in production
        if not settings.DEBUG:
            media_root = settings.MEDIA_ROOT
            if not os.path.exists(media_root):
                raise FileNotFoundError(
                    f"Media directory {media_root} not found. "
                    "Ensure Render Persistent Disk is properly mounted."
                )
        
        super().__init__(**kwargs)
