import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from django.conf import settings
from marketplace.models import Product

print("=== MEDIA URL AND FILE TEST ===")

# Check settings
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"STATIC_URL: {settings.STATIC_URL}")

# Check if media directory exists
if os.path.exists(settings.MEDIA_ROOT):
    print(f"✅ Media directory exists: {settings.MEDIA_ROOT}")
    products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
    if os.path.exists(products_dir):
        files = os.listdir(products_dir)
        print(f"✅ Products directory exists with {len(files)} files")
        
        # Test first 3 files
        for file in files[:3]:
            file_path = os.path.join(products_dir, file)
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"  ✅ {file}: {size} bytes")
            else:
                print(f"  ❌ {file}: File not found")
    else:
        print(f"❌ Products directory does not exist: {products_dir}")
else:
    print(f"❌ Media directory does not exist: {settings.MEDIA_ROOT}")

# Test database products
print("\n=== DATABASE PRODUCTS ===")
products = Product.objects.all()
print(f"Total products in database: {products.count()}")

for product in products[:3]:
    print(f"\nProduct: {product.name}")
    if product.image:
        print(f"  Image field: {product.image}")
        print(f"  Image name: {product.image.name}")
        if hasattr(product.image, 'url'):
            print(f"  Image URL: {product.image.url}")
            
            # Check if file actually exists
            full_path = os.path.join(settings.MEDIA_ROOT, product.image.name)
            if os.path.exists(full_path):
                size = os.path.getsize(full_path)
                print(f"  ✅ File exists: {size} bytes")
            else:
                print(f"  ❌ File not found: {full_path}")
        else:
            print("  ❌ No URL attribute")
    else:
        print("  ❌ No image")

print("\n=== URL GENERATION TEST ===")
# Test URL generation
from django.templatetags.static import static
placeholder_url = static('img/product-placeholder.jpg')
print(f"Product placeholder URL: {placeholder_url}")

# Test media URL generation
if products.exists():
    first_product = products.first()
    if first_product.image:
        print(f"Sample product media URL: {first_product.image.url}")
