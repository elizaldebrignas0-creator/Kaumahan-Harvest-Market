import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from django.conf import settings
from marketplace.models import Product

print("=== IMAGE LOADING DIAGNOSIS ===")

# Check settings
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"DEBUG: {settings.DEBUG}")

# Check media directory
media_products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
if os.path.exists(media_products_dir):
    files = os.listdir(media_products_dir)
    print(f"✅ Media/products directory exists with {len(files)} files")
    print(f"Files: {files[:5]}...")  # Show first 5 files
else:
    print(f"❌ Media/products directory not found: {media_products_dir}")

# Check database products
print("\n=== DATABASE PRODUCTS ===")
products = Product.objects.all()
print(f"Total products: {products.count()}")

for i, product in enumerate(products[:3]):
    print(f"\nProduct {i+1}: {product.name}")
    print(f"  Image field: {product.image}")
    if product.image:
        print(f"  Image name: {product.image.name}")
        if hasattr(product.image, 'url'):
            print(f"  Image URL: {product.image.url}")
            
            # Check if file exists
            full_path = os.path.join(settings.MEDIA_ROOT, product.image.name)
            if os.path.exists(full_path):
                size = os.path.getsize(full_path)
                print(f"  ✅ File exists: {size} bytes")
            else:
                print(f"  ❌ File NOT found: {full_path}")
        else:
            print(f"  ❌ No URL attribute")
    else:
        print(f"  ❌ No image")

# Test URL generation
print("\n=== URL GENERATION TEST ===")
from django.templatetags.static import static
placeholder_url = static('img/product-placeholder.jpg')
print(f"Product placeholder URL: {placeholder_url}")

# Check if there are any logo files in media products
logo_files = [f for f in os.listdir(media_products_dir) if 'logo' in f.lower() or 'banner' in f.lower()]
if logo_files:
    print(f"⚠️  Found potentially problematic files in media/products: {logo_files}")
else:
    print("✅ No logo/banner files found in media/products")
