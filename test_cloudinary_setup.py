"""
Quick test to verify Cloudinary setup is working
"""

import os
import django

# Set up Django with Cloudinary settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings_cloudinary')
django.setup()

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from marketplace.models import Product

def test_cloudinary_setup():
    print("=== CLOUDINARY SETUP TEST ===")
    
    # Test basic configuration
    print(f"\n📋 Configuration:")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    
    # Test Cloudinary settings
    print(f"\n☁️ Cloudinary Settings:")
    print(f"CLOUDINARY_CLOUD_NAME: {getattr(settings, 'CLOUDINARY_CLOUD_NAME', 'Not set')}")
    print(f"CLOUDINARY_API_KEY: {'Set' if getattr(settings, 'CLOUDINARY_API_KEY', None) else 'Not set'}")
    print(f"CLOUDINARY_API_SECRET: {'Set' if getattr(settings, 'CLOUDINARY_API_SECRET', None) else 'Not set'}")
    
    # Test storage backend
    print(f"\n🔧 Storage Backend:")
    try:
        from storages.backends.cloudinary_storage import CloudinaryStorage
        storage = CloudinaryStorage()
        print(f"✅ Cloudinary storage initialized: {storage.__class__.__name__}")
    except Exception as e:
        print(f"❌ Storage backend error: {e}")
        return False
    
    # Test file upload simulation
    print(f"\n📤 Upload Test:")
    try:
        # Create a test image
        test_image = SimpleUploadedFile(
            "test_product.jpg", 
            b"fake_image_content_for_testing", 
            content_type="image/jpeg"
        )
        
        # Test saving to Cloudinary
        saved_path = storage.save('products/test_product.jpg', test_image)
        print(f"✅ Test file saved to: {saved_path}")
        
        # Test URL generation
        file_url = storage.url(saved_path)
        print(f"✅ File URL: {file_url}")
        
        # Verify it's a Cloudinary URL
        if 'cloudinary' in file_url:
            print(f"✅ URL is from Cloudinary")
        else:
            print(f"⚠️ URL might be local: {file_url}")
        
        # Clean up
        storage.delete(saved_path)
        print(f"✅ Test file cleaned up")
        
    except Exception as e:
        print(f"❌ Upload test failed: {e}")
        return False
    
    # Test model field
    print(f"\n📋 Model Field Test:")
    try:
        product_image_field = Product._meta.get_field('image')
        print(f"✅ Product image field: {product_image_field}")
        print(f"Storage: {product_image_field.storage}")
    except Exception as e:
        print(f"❌ Model field test failed: {e}")
    
    print(f"\n✅ Cloudinary setup test completed!")
    return True

if __name__ == '__main__':
    test_cloudinary_setup()
