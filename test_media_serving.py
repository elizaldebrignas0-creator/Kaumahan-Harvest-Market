import requests
import os

print("=== TESTING MEDIA FILE SERVING ===")

# Test if the specific eggplant image can be accessed
test_urls = [
    "http://127.0.0.1:8000/media/products/eggplant_gLa4bMg.jpg",
    "http://127.0.0.1:8000/media/products/1000013097_qY4O9Br.jpg",
    "http://127.0.0.1:8000/static/img/product-placeholder.jpg"
]

for url in test_urls:
    try:
        print(f"\n🔗 Testing: {url}")
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            print(f"  ✅ Success (Status: {response.status_code})")
            print(f"  Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
            print(f"  Content-Length: {response.headers.get('Content-Length', 'Unknown')} bytes")
        else:
            print(f"  ❌ Failed (Status: {response.status_code})")
            print(f"  Response: {response.text[:100]}...")
            
    except requests.exceptions.ConnectionError:
        print(f"  ❌ Connection refused - server not running")
        break
    except requests.exceptions.Timeout:
        print(f"  ❌ Request timed out")
    except Exception as e:
        print(f"  ❌ Error: {e}")

# Test home page to see what images are being referenced
try:
    print(f"\n🏠 Testing home page...")
    response = requests.get("http://127.0.0.1:8000/", timeout=5)
    
    if response.status_code == 200:
        if '/media/products/eggplant_gLa4bMg.jpg' in response.text:
            print("  ✅ Eggplant image found in home page HTML")
        else:
            print("  ❌ Eggplant image NOT found in home page HTML")
            
        if 'product-placeholder.jpg' in response.text:
            print("  ⚠️  Placeholder found in HTML (may be fallback)")
    else:
        print(f"  ❌ Home page failed: {response.status_code}")
        
except Exception as e:
    print(f"  ❌ Error testing home page: {e}")
