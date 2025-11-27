"""
Migration to ensure media consistency and fix image paths
"""

from django.db import migrations
import os
from django.conf import settings


def ensure_media_directories(apps, schema_editor):
    """Ensure media directories exist"""
    media_root = settings.MEDIA_ROOT
    directories = ['products', 'business_permits', 'avatars', 'temp']
    
    for directory in directories:
        dir_path = os.path.join(media_root, directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"Created directory: {dir_path}")


def verify_product_images(apps, schema_editor):
    """Verify product image paths are correct"""
    Product = apps.get_model('marketplace', 'Product')
    
    for product in Product.objects.all():
        if product.image:
            # Ensure image path starts with products/
            if not product.image.name.startswith('products/'):
                old_path = product.image.name
                new_path = f"products/{os.path.basename(old_path)}"
                product.image.name = new_path
                product.save()
                print(f"Updated product {product.id} image path: {old_path} -> {new_path}")


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),  # Replace with your latest migration
    ]

    operations = [
        migrations.RunPython(ensure_media_directories),
        migrations.RunPython(verify_product_images),
    ]
