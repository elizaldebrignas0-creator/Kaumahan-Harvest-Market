#!/usr/bin/env python
import os
import sys
import django
import shutil

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from marketplace.models import Product
from django.contrib.auth import get_user_model
from django.core.files import File

def setup_production_media():
    print("=== Setting up Production Media ===")
    
    # Ensure media directories exist
    media_root = "media"
    products_dir = os.path.join(media_root, "products")
    
    os.makedirs(products_dir, exist_ok=True)
    print(f"Media directories created: {products_dir}")
    
    # Copy sample images from static if they exist
    static_img_dir = "static/img"
    if os.path.exists(static_img_dir):
        for file in os.listdir(static_img_dir):
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                src = os.path.join(static_img_dir, file)
                dst = os.path.join(products_dir, file)
                shutil.copy2(src, dst)
                print(f"Copied {file} to media/products/")
    
    # Create a default product image if none exist
    default_images = [
        "eggplant.jpg",
        "chicken.jpg", 
        "vegetables.jpg"
    ]
    
    for img_name in default_images:
        img_path = os.path.join(products_dir, img_name)
        if not os.path.exists(img_path):
            # Create a simple placeholder image file
            from PIL import Image
            import io
            
            # Create a simple colored square as placeholder
            img = Image.new('RGB', (300, 300), color='green')
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')
            img_bytes.seek(0)
            
            with open(img_path, 'wb') as f:
                f.write(img_bytes.getvalue())
            print(f"Created placeholder: {img_name}")
    
    # Update products to have images
    User = get_user_model()
    seller = User.objects.filter(user_type='seller').first()
    
    if seller:
        products = Product.objects.all()
        for i, product in enumerate(products):
            if not product.image and i < len(default_images):
                img_path = os.path.join(products_dir, default_images[i])
                if os.path.exists(img_path):
                    with open(img_path, 'rb') as f:
                        product.image.save(default_images[i], File(f), save=True)
                    print(f"Assigned {default_images[i]} to {product.name}")
    
    print("\n=== Production Media Setup Complete ===")

if __name__ == "__main__":
    setup_production_media()
