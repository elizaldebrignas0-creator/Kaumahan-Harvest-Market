"""
Test AWS S3 storage configuration
"""

import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

def test_s3_storage():
    print("=== AWS S3 STORAGE TEST ===")
    
    # Check configuration
    print(f"\n📋 Configuration:")
    print(f"Environment: {'Production' if not settings.DEBUG else 'Development'}")
    print(f"Storage backend: {settings.DEFAULT_FILE_STORAGE}")
    print(f"Media URL: {settings.MEDIA_URL}")
    
    if not settings.DEBUG:
        print(f"AWS Bucket: {settings.AWS_STORAGE_BUCKET_NAME}")
        print(f"AWS Region: {settings.AWS_S3_REGION_NAME}")
    
    # Test file upload
    print(f"\n📤 File Upload Test:")
    try:
        # Create test image
        test_image = SimpleUploadedFile(
            "test_product.jpg", 
            b"fake_image_content_for_testing", 
            content_type="image/jpeg"
        )
        
        # Save to storage
        saved_path = default_storage.save('products/test_product.jpg', test_image)
        print(f"✅ File saved to: {saved_path}")
        
        # Get URL
        file_url = default_storage.url(saved_path)
        print(f"✅ File URL: {file_url}")
        
        # Check if exists
        exists = default_storage.exists(saved_path)
        print(f"✅ File exists: {exists}")
        
        # Clean up
        default_storage.delete(saved_path)
        print(f"✅ Test file deleted")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    print(f"\n✅ S3 storage test complete!")

if __name__ == '__main__':
    test_s3_storage()
