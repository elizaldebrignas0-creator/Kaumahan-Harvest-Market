import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from marketplace.models import Product
from django.conf import settings

print("=== DEBUGGING EGGPLANT IMAGE ISSUE ===")

# Find the eggplant product
eggplant_products = Product.objects.filter(name__icontains='eggplant')
print(f"Found {eggplant_products.count()} eggplant products:")

for product in eggplant_products:
    print(f"\n📦 Product: {product.name}")
    print(f"  ID: {product.id}")
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
        print(f"  ❌ No image at all")

# Check what the template should render
print(f"\n📝 Template Logic Test:")
for product in eggplant_products:
    if product.image and hasattr(product.image, 'url') and product.image.url:
        result = product.image.url
        print(f"  {product.name}: Should render {result}")
    else:
        print(f"  {product.name}: Should render placeholder")

# Check all products to see which one might be causing issues
print(f"\n🔍 All Products Check:")
all_products = Product.objects.all()
for product in all_products:
    print(f"  {product.name}: {product.image.url if product.image and hasattr(product.image, 'url') else 'NO IMAGE'}")
