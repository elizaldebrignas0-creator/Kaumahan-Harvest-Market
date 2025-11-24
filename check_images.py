import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from marketplace.models import Product

print("=== PRODUCT IMAGE CHECK ===")
products = Product.objects.all()
print(f"Total products: {products.count()}")

for i, product in enumerate(products[:5]):
    print(f"\nProduct {i+1}:")
    print(f"  Name: {product.name}")
    print(f"  Image field: {product.image}")
    if product.image:
        print(f"  Image name: {product.image.name}")
        if hasattr(product.image, 'url'):
            print(f"  Image URL: {product.image.url}")
        else:
            print("  No URL attribute")
    else:
        print("  No image")

print("\n=== MEDIA DIRECTORY CHECK ===")
media_products_dir = "media/products"
if os.path.exists(media_products_dir):
    files = os.listdir(media_products_dir)
    print(f"Files in {media_products_dir}: {len(files)}")
    for file in files[:5]:
        print(f"  - {file}")
else:
    print(f"Directory {media_products_dir} does not exist")
