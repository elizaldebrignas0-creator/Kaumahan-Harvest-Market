#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from marketplace.models import Product
from django.conf import settings

def check_media_files():
    print("=== Complete Media File Check ===")
    
    # Check Django settings
    print(f"DEBUG: {settings.DEBUG}")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    
    # Check if media directory exists
    media_exists = os.path.exists(settings.MEDIA_ROOT)
    print(f"Media directory exists: {media_exists}")
    
    if not media_exists:
        print("Creating media directory...")
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    
    # Check products directory
    products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
    products_exists = os.path.exists(products_dir)
    print(f"Products directory exists: {products_exists}")
    
    if not products_exists:
        print("Creating products directory...")
        os.makedirs(products_dir, exist_ok=True)
    
    # List all files in media directory
    print(f"\nFiles in media directory:")
    media_root_str = str(settings.MEDIA_ROOT)
    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
        root_str = str(root)
        level = root_str.replace(media_root_str, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            print(f"{subindent}{file} ({file_size} bytes)")
    
    # Check products with images
    products = Product.objects.all()
    print(f"\nTotal products: {products.count()}")
    
    for product in products:
        print(f"\nProduct: {product.name}")
        print(f"  Has image field: {bool(product.image)}")
        
        if product.image:
            print(f"  Image name: {product.image.name}")
            print(f"  Image URL: {product.image.url}")
            print(f"  Image path: {product.image.path}")
            
            # Check if file exists
            file_exists = os.path.exists(product.image.path)
            print(f"  File exists: {file_exists}")
            
            if file_exists:
                file_size = os.path.getsize(product.image.path)
                print(f"  File size: {file_size} bytes")
            else:
                print(f"  ERROR: File does not exist at {product.image.path}")
                
                # Try to create the file if it doesn't exist
                print(f"  Attempting to fix missing file...")
                try:
                    # Copy from existing files if available
                    existing_files = []
                    for root, dirs, files in os.walk(products_dir):
                        for file in files:
                            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                                existing_files.append(os.path.join(root, file))
                    
                    if existing_files:
                        import shutil
                        src = existing_files[0]
                        dst = product.image.path
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.copy2(src, dst)
                        print(f"  Copied {src} to {dst}")
                    else:
                        print(f"  No existing files to copy from")
                except Exception as e:
                    print(f"  Error fixing file: {e}")
        else:
            print("  No image associated")

if __name__ == "__main__":
    check_media_files()
