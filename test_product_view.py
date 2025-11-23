#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from marketplace.models import Product
from marketplace.views import product_detail

def test_product_view():
    print("=== Testing Product Detail View ===")
    
    # Get the test product
    product = Product.objects.first()
    if not product:
        print("No products found!")
        return
    
    print(f"Testing product: {product.name} (ID: {product.id})")
    
    # Get a user for authentication
    User = get_user_model()
    user = User.objects.first()
    if not user:
        print("No users found!")
        return
    
    print(f"Using user: {user.email}")
    
    # Create a mock request with authentication
    factory = RequestFactory()
    request = factory.get(f'/marketplace/products/{product.id}/')
    request.user = user  # Add user to request
    
    # Test the view
    try:
        response = product_detail(request, product.id)
        print(f"View executed successfully!")
        print(f"Response status: {response.status_code if hasattr(response, 'status_code') else 'N/A'}")
        print(f"Template used: {getattr(response, 'template_name', 'N/A')}")
        
        # Check if product is in context
        if hasattr(response, 'context_data'):
            context_product = response.context_data.get('product')
            if context_product:
                print(f"Product in context: {context_product.name}")
            else:
                print("Product not found in context!")
        
    except Exception as e:
        print(f"Error executing view: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_product_view()
