import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from django.conf import settings
from marketplace.models import Product
from django.templatetags.static import static

print("=== SIMPLE IMAGE CONSISTENCY TEST ===")

# Test 1: Verify database and file system
products = Product.objects.all()
print(f"Testing {products.count()} products...")

all_good = True
for product in products:
    print(f"\n📦 {product.name}")
    
    if product.image and hasattr(product.image, 'url'):
        image_url = product.image.url
        print(f"  ✅ URL: {image_url}")
        
        # Verify it's the correct format
        if image_url.startswith('/media/products/'):
            print(f"  ✅ Correct URL format")
        else:
            print(f"  ❌ Wrong URL format")
            all_good = False
        
        # Check file exists
        full_path = os.path.join(settings.MEDIA_ROOT, product.image.name)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            print(f"  ✅ File exists: {size} bytes")
        else:
            print(f"  ❌ File missing")
            all_good = False
    else:
        print(f"  ⚠️  No image - will use placeholder")

# Test 2: Verify placeholder
placeholder_url = static('img/product-placeholder.jpg')
print(f"\n🖼️  Placeholder URL: {placeholder_url}")

# Test 3: Simulate what templates will render
print(f"\n📝 Template Rendering Simulation:")
for product in products[:2]:
    if product.image and hasattr(product.image, 'url') and product.image.url:
        result = product.image.url
        print(f"  {product.name}: <img src=\"{result}\" alt=\"{product.name}\">")
    else:
        result = placeholder_url
        print(f"  {product.name}: <img src=\"{result}\" alt=\"{product.name}\">")

# Test 4: Check media serving configuration
print(f"\n⚙️  Configuration Check:")
print(f"  MEDIA_URL: {settings.MEDIA_URL}")
print(f"  MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"  DEBUG: {settings.DEBUG}")

# Test 5: Verify no problematic files
media_products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
if os.path.exists(media_products_dir):
    files = os.listdir(media_products_dir)
    problematic = [f for f in files if any(x in f.lower() for x in ['logo', 'banner', 'favicon'])]
    if problematic:
        print(f"  ❌ Found problematic files: {problematic}")
        all_good = False
    else:
        print(f"  ✅ No problematic files in media/products")

print(f"\n{'='*50}")
if all_good:
    print("✅ ALL TESTS PASSED - Images should load consistently!")
else:
    print("❌ Some tests failed - check the issues above")

print(f"\n📋 Next Steps:")
print("1. Restart development server: python manage.py runserver")
print("2. Open browser console and run: window.checkImages()")
print("3. Test page refresh multiple times")
print("4. Images should remain consistent and not disappear")
