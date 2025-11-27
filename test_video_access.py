import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from django.conf import settings
from django.templatetags.static import static

print("=== VIDEO ACCESSIBILITY TEST ===")

# Test the video file path
video_path = "static/img/advertisement.mp4"
full_path = os.path.join(settings.BASE_DIR, video_path)

print(f"📁 File Path: {video_path}")
print(f"📍 Full Path: {full_path}")
print(f"✅ File Exists: {os.path.exists(full_path)}")

if os.path.exists(full_path):
    size = os.path.getsize(full_path)
    print(f"📏 File Size: {size:,} bytes ({size/1024/1024:.2f} MB)")

# Test static URL generation
try:
    video_url = static('img/advertisement.mp4')
    print(f"🌐 Static URL: {video_url}")
    print(f"✅ URL Generation: Success")
except Exception as e:
    print(f"❌ URL Generation Failed: {e}")

# Test Django settings
print(f"\n⚙️ Django Settings:")
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"DEBUG: {settings.DEBUG}")
print(f"STATICFILES_DIRS: {getattr(settings, 'STATICFILES_DIRS', 'Not set')}")

# Create a simple HTML test
test_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Video Test Page</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .video-container {{ max-width: 800px; margin: 0 auto; }}
        video {{ width: 100%; border: 2px solid #ccc; }}
        .status {{ margin: 10px 0; padding: 10px; background: #f0f0f0; }}
    </style>
</head>
<body>
    <h1>Video Playback Test</h1>
    <div class="status">
        <strong>Expected URL:</strong> {video_url if 'video_url' in locals() else '/static/img/advertisement.mp4'}<br>
        <strong>File Size:</strong> {size if 'size' in locals() else 'Unknown'}
    </div>
    
    <div class="video-container">
        <video controls preload="metadata" poster="/static/img/banner.png" style="width: 100%;">
            <source src="{video_url if 'video_url' in locals() else '/static/img/advertisement.mp4'}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
    </div>
    
    <div class="status">
        <h3>Test Instructions:</h3>
        <ol>
            <li>Check if the poster image appears</li>
            <li>Click the play button</li>
            <li>Check browser console for errors</li>
            <li>Try downloading: <a href="{video_url if 'video_url' in locals() else '/static/img/advertisement.mp4'}" target="_blank">Direct Link</a></li>
        </ol>
    </div>
    
    <script>
        const video = document.querySelector('video');
        video.addEventListener('loadstart', () => console.log('Video loading started'));
        video.addEventListener('loadedmetadata', () => console.log('Video metadata loaded'));
        video.addEventListener('canplay', () => console.log('Video can play'));
        video.addEventListener('error', (e) => {{
            console.error('Video error:', e);
            console.error('Error code:', video.error ? video.error.code : 'Unknown');
        }});
        
        // Check ready state after 3 seconds
        setTimeout(() => {{
            console.log('Video ready state:', video.readyState);
            console.log('Video network state:', video.networkState);
        }}, 3000);
    </script>
</body>
</html>
"""

with open('video_access_test.html', 'w') as f:
    f.write(test_html)

print(f"\n🧪 Created video_access_test.html")
print(f"Open this file in your browser to test video playback")
print(f"Run 'python manage.py runserver' and visit http://127.0.0.1:8000/static/video_access_test.html")

print(f"\n✅ Video accessibility test complete!")
