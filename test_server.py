#!/usr/bin/env python
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from django.test import Client
from marketplace.models import Product
from django.urls import reverse

def test_media_serving():
    print("=== Testing Media Serving ===")
    
    client = Client()
    
    # Get a product with an image
    product = Product.objects.filter(image__isnull=False).first()
    if not product:
        print("No products with images found!")
        return
    
    print(f"Testing product: {product.name}")
    print(f"Image URL: {product.image.url}")
    
    # Test the media URL directly
    try:
        response = client.get(product.image.url)
        print(f"Response status: {response.status_code}")
        print(f"Content-Type: {response.get('Content-Type')}")
        print(f"Content-Length: {len(response.content)}")
        
        if response.status_code == 200:
            print("✅ Media serving works!")
        else:
            print("❌ Media serving failed!")
            print(f"Response content: {response.content[:200]}...")
            
    except Exception as e:
        print(f"❌ Error testing media serving: {e}")
    
    # Test the custom media serve view directly
    try:
        from marketplace.views import custom_media_serve
        from django.http import HttpRequest
        
        request = HttpRequest()
        request.method = 'GET'
        
        # Extract the path from the image URL
        path = product.image.name  # This should be 'products/filename.jpg'
        print(f"Testing custom view with path: {path}")
        
        response = custom_media_serve(request, path)
        print(f"Custom view status: {response.status_code}")
        print(f"Custom view Content-Type: {response.get('Content-Type')}")
        
        if response.status_code == 200:
            print("✅ Custom media serving works!")
        else:
            print("❌ Custom media serving failed!")
            
    except Exception as e:
        print(f"❌ Error testing custom media serving: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_media_serving()
