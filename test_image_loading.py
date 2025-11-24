import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from marketplace.models import Product

print("=== IMAGE LOADING TEST ===")

# Test each product's image
products = Product.objects.all()
print(f"Testing {products.count()} products...")

for product in products:
    print(f"\n📦 Product: {product.name}")
    
    if product.image and hasattr(product.image, 'url'):
        image_url = product.image.url
        print(f"  ✅ Image URL: {image_url}")
        
        # Check if URL starts with /media/products/
        if image_url.startswith('/media/products/'):
            print(f"  ✅ Correct URL format")
        else:
            print(f"  ❌ Wrong URL format: {image_url}")
        
        # Check if file exists
        from django.conf import settings
        full_path = os.path.join(settings.MEDIA_ROOT, product.image.name)
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            print(f"  ✅ File exists: {size} bytes")
        else:
            print(f"  ❌ File NOT found: {full_path}")
    else:
        print(f"  ⚠️  No image - should use placeholder")

print("\n=== TEMPLATE TEST ===")
# Test what template would render
from django.templatetags.static import static
placeholder_url = static('img/product-placeholder.jpg')
print(f"Placeholder URL: {placeholder_url}")

# Simulate template logic
for product in products[:2]:
    print(f"\nTemplate render for: {product.name}")
    if product.image and product.image.url:
        result = product.image.url
        print(f"  Would render: {result}")
    else:
        result = placeholder_url
        print(f"  Would render placeholder: {result}")

print("\n✅ All tests completed!")
