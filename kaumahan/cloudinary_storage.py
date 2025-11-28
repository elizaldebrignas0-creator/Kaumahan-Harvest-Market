"""
Cloudinary storage backend for Django
Easy setup for media file storage in production
"""

import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.core.files.storage import Storage
from django.conf import settings
from io import BytesIO


class CloudinaryStorage(Storage):
    """
    Cloudinary storage backend for Django
    """
    
    def __init__(self):
        if not settings.DEBUG:
            # Configure Cloudinary in production
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                api_key=settings.CLOUDINARY_API_KEY,
                api_secret=settings.CLOUDINARY_API_SECRET
            )
    
    def _save(self, name, content):
        """
        Save file to Cloudinary
        """
        if settings.DEBUG:
            # Local development - save to filesystem
            return super()._save(name, content)
        
        # Production - upload to Cloudinary
        try:
            # Read file content
            content.seek(0)
            file_content = content.read()
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                file_content,
                public_id=name,
                folder='media/products/',
                resource_type='image',
                format='jpg'
            )
            
            # Return the public ID
            return result['public_id']
            
        except Exception as e:
            print(f"Cloudinary upload error: {e}")
            raise
    
    def url(self, name):
        """
        Get URL for the file
        """
        if settings.DEBUG:
            # Local development
            return f"{settings.MEDIA_URL}{name}"
        
        # Production - Cloudinary URL
        try:
            result = cloudinary.api.resource(name)
            return result['secure_url']
        except Exception:
            # Fallback URL
            return f"https://res.cloudinary.com/{settings.CLOUDINARY_CLOUD_NAME}/image/upload/{name}"
    
    def exists(self, name):
        """
        Check if file exists
        """
        if settings.DEBUG:
            # Local development
            import os
            return os.path.exists(os.path.join(settings.MEDIA_ROOT, name))
        
        # Production - check Cloudinary
        try:
            cloudinary.api.resource(name)
            return True
        except Exception:
            return False
    
    def delete(self, name):
        """
        Delete file from Cloudinary
        """
        if settings.DEBUG:
            # Local development
            import os
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
            return
        
        # Production - delete from Cloudinary
        try:
            cloudinary.api.delete_resources([name])
        except Exception as e:
            print(f"Cloudinary delete error: {e}")
