import requests
import os

print("=== DEVELOPMENT SERVER MEDIA FILE TEST ===")

# Test if development server is running and serving media files
try:
    # Test a specific media file
    test_url = "http://127.0.0.1:8000/media/products/eggplant_gLa4bMg.jpg"
    print(f"Testing URL: {test_url}")
    
    response = requests.get(test_url, timeout=5)
    
    if response.status_code == 200:
        print(f"✅ Media file served successfully (Status: {response.status_code})")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
        print(f"   Content-Length: {response.headers.get('Content-Length', 'Unknown')} bytes")
    else:
        print(f"❌ Media file failed to load (Status: {response.status_code})")
        print(f"   Response: {response.text[:200]}...")
        
except requests.exceptions.ConnectionError:
    print("❌ Development server not running or not accessible")
    print("   Please start the development server with: python manage.py runserver")
except requests.exceptions.Timeout:
    print("❌ Request timed out - server may be slow to respond")
except Exception as e:
    print(f"❌ Error testing media file: {e}")

# Test static file serving
try:
    static_url = "http://127.0.0.1:8000/static/img/product-placeholder.jpg"
    print(f"\nTesting static URL: {static_url}")
    
    response = requests.get(static_url, timeout=5)
    
    if response.status_code == 200:
        print(f"✅ Static file served successfully (Status: {response.status_code})")
    else:
        print(f"❌ Static file failed to load (Status: {response.status_code})")
        
except Exception as e:
    print(f"❌ Error testing static file: {e}")

# Test home page
try:
    home_url = "http://127.0.0.1:8000/"
    print(f"\nTesting home page: {home_url}")
    
    response = requests.get(home_url, timeout=5)
    
    if response.status_code == 200:
        print(f"✅ Home page loaded successfully (Status: {response.status_code})")
        
        # Check if page contains product images
        if 'media/products/' in response.text:
            print("✅ Page contains media/product image references")
        else:
            print("⚠️  No media/product image references found in page")
            
        if 'product-placeholder.jpg' in response.text:
            print("✅ Page contains product placeholder references")
        else:
            print("⚠️  No product placeholder references found in page")
    else:
        print(f"❌ Home page failed to load (Status: {response.status_code})")
        
except Exception as e:
    print(f"❌ Error testing home page: {e}")
