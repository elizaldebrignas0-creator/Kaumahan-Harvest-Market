import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from django.conf import settings
from marketplace.models import Product

print("=== FIXING IMAGE CONSISTENCY ===")

# Step 1: Verify all product images are correctly saved
products = Product.objects.all()
print(f"Checking {products.count()} products...")

for product in products:
    print(f"\n📦 {product.name}")
    
    if product.image:
        print(f"  Current image field: {product.image}")
        print(f"  Image name: {product.image.name}")
        
        # Check if file exists
        full_path = os.path.join(settings.MEDIA_ROOT, product.image.name)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            print(f"  ✅ File exists: {size} bytes")
        else:
            print(f"  ❌ File missing: {full_path}")
            
        # Check URL generation
        if hasattr(product.image, 'url'):
            print(f"  ✅ URL: {product.image.url}")
        else:
            print(f"  ❌ No URL attribute")
    else:
        print(f"  ⚠️  No image - will use placeholder")

# Step 2: Check for any problematic files in media directory
media_products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
if os.path.exists(media_products_dir):
    files = os.listdir(media_products_dir)
    print(f"\n📁 Files in media/products/: {len(files)}")
    
    # Check for any problematic files
    problematic = [f for f in files if any(x in f.lower() for x in ['logo', 'banner', 'favicon'])]
    if problematic:
        print(f"⚠️  Found problematic files: {problematic}")
    else:
        print("✅ No problematic files found")

# Step 3: Test actual URL generation
print(f"\n🔗 URL Generation Test:")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")

from django.templatetags.static import static
placeholder_url = static('img/product-placeholder.jpg')
print(f"Placeholder URL: {placeholder_url}")

# Step 4: Create a simple test template rendering
print(f"\n📝 Template Rendering Test:")
for product in products[:2]:
    if product.image and hasattr(product.image, 'url'):
        result = product.image.url
        print(f"  {product.name}: {result}")
    else:
        result = placeholder_url
        print(f"  {product.name}: {result} (placeholder)")

print("\n✅ Diagnosis complete!")
