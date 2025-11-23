#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from django.contrib.auth import get_user_model
from marketplace.models import Product

def debug_products():
    print("=== Product Debug Investigation ===")
    
    # Check users
    User = get_user_model()
    users = User.objects.all()
    print(f"Total users: {users.count()}")
    
    # Find seller users
    sellers = []
    for user in users:
        print(f"User: {user.email}, Type: {getattr(user, 'user_type', 'Unknown')}, is_seller: {getattr(user, 'is_seller', False)}")
        if hasattr(user, 'user_type') and user.user_type == 'seller':
            sellers.append(user)
            print(f"Seller found: {user.email} (ID: {user.id})")
        elif hasattr(user, 'is_seller') and user.is_seller:
            sellers.append(user)
            print(f"Seller found: {user.email} (ID: {user.id})")
    
    # Create a seller user if none exist
    if not sellers and users.count() > 0:
        print("\nCreating a seller user...")
        user = users.first()
        if hasattr(user, 'user_type'):
            user.user_type = 'seller'
        elif hasattr(user, 'is_seller'):
            user.is_seller = True
        user.save()
        sellers.append(user)
        print(f"Converted user to seller: {user.email}")
    
    # Check all products
    all_products = Product.objects.all()
    print(f"\nTotal products in database: {all_products.count()}")
    
    for product in all_products:
        print(f"  - {product.name} (ID: {product.id}, Seller: {product.seller.email}, Active: {product.is_active})")
    
    # Create a test product if none exist
    if all_products.count() == 0 and sellers:
        print("\nCreating test product...")
        seller = sellers[0]
        test_product = Product.objects.create(
            name="Test Eggplant",
            description="Fresh eggplant from local farm",
            price=145.00,
            category="VEGETABLES",
            unit="KG",
            seller=seller
        )
        print(f"Created test product: {test_product.name} (ID: {test_product.id})")
        
        # Test the URL
        from django.urls import reverse
        product_url = reverse('product_detail', kwargs={'pk': test_product.id})
        print(f"Product detail URL: {product_url}")
    
    print("\n=== Debug Complete ===")

if __name__ == "__main__":
    debug_products()
