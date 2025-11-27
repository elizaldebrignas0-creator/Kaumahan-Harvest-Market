"""
Test script to verify media storage configuration
"""

import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from marketplace.models import Product

def test_media_configuration():
    print("=== MEDIA STORAGE CONFIGURATION TEST ===")
    
    # Test basic settings
    print(f"\n📁 Basic Configuration:")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Default')}")
    
    # Test storage backend
    print(f"\n🔧 Storage Backend:")
    try:
        from kaumahan.storage import RenderPersistentStorage, RenderProductionStorage
        print(f"✅ Custom storage classes imported successfully")
        
        # Test storage instantiation
        if settings.DEBUG:
            storage = RenderPersistentStorage()
            print(f"✅ Development storage initialized: {storage.__class__.__name__}")
        else:
            storage = RenderProductionStorage()
            print(f"✅ Production storage initialized: {storage.__class__.__name__}")
            
    except Exception as e:
        print(f"❌ Storage backend error: {e}")
    
    # Test directory structure
    print(f"\n📂 Directory Structure:")
    media_root = settings.MEDIA_ROOT
    print(f"Media root exists: {os.path.exists(media_root)}")
    
    if os.path.exists(media_root):
        products_dir = os.path.join(media_root, 'products')
        print(f"Products directory exists: {os.path.exists(products_dir)}")
        
        # List contents
        try:
            contents = os.listdir(media_root)
            print(f"Media root contents: {contents}")
        except Exception as e:
            print(f"❌ Error listing media root: {e}")
    
    # Test file upload simulation
    print(f"\n📤 File Upload Test:")
    try:
        # Create a test image
        test_image = SimpleUploadedFile(
            "test_product.jpg", 
            b"fake_image_content", 
            content_type="image/jpeg"
        )
        
        # Test storage save
        storage = settings.DEFAULT_FILE_STORAGE
        if isinstance(storage, str):
            from django.core.files.storage import default_storage
            storage = default_storage
        
        # Test saving
        saved_path = storage.save('products/test_product.jpg', test_image)
        print(f"✅ Test file saved to: {saved_path}")
        
        # Test URL generation
        file_url = storage.url(saved_path)
        print(f"✅ File URL: {file_url}")
        
        # Test file existence
        exists = storage.exists(saved_path)
        print(f"✅ File exists: {exists}")
        
        # Clean up
        storage.delete(saved_path)
        print(f"✅ Test file cleaned up")
        
    except Exception as e:
        print(f"❌ File upload test failed: {e}")
    
    # Test model field configuration
    print(f"\n📋 Model Field Configuration:")
    try:
        product_image_field = Product._meta.get_field('image')
        print(f"✅ Product image field: {product_image_field}")
        print(f"Upload to: {product_image_field.upload_to}")
        print(f"Storage: {product_image_field.storage}")
    except Exception as e:
        print(f"❌ Model field test failed: {e}")
    
    print(f"\n✅ Media configuration test complete!")

if __name__ == '__main__':
    test_media_configuration()
