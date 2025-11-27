import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings')
django.setup()

from django.conf import settings
from django.templatetags.static import static

print("=== DJANGO STATIC VIDEO SERVING TEST ===")

# 1. Check Django static configuration
print(f"\n⚙️  Django Configuration:")
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"DEBUG: {settings.DEBUG}")

# 2. Check static file path resolution
video_static_path = 'img/advertisement.mp4'
video_full_path = os.path.join(settings.BASE_DIR, 'static', video_static_path)

print(f"\n📁 Static File Path Analysis:")
print(f"Template path: {video_static_path}")
print(f"Full filesystem path: {video_full_path}")
print(f"File exists: {os.path.exists(video_full_path)}")

if os.path.exists(video_full_path):
    size = os.path.getsize(video_full_path)
    print(f"File size: {size:,} bytes ({size/1024/1024:.2f} MB)")

# 3. Test static URL generation
try:
    video_url = static(video_static_path)
    print(f"\n🌐 Static URL Generation:")
    print(f"Generated URL: {video_url}")
    print(f"URL starts with STATIC_URL: {video_url.startswith(settings.STATIC_URL)}")
except Exception as e:
    print(f"\n❌ Static URL generation failed: {e}")

# 4. Check static files directory structure
static_img_dir = os.path.join(settings.BASE_DIR, 'static', 'img')
if os.path.exists(static_img_dir):
    files = os.listdir(static_img_dir)
    print(f"\n📂 Static/img directory contents:")
    for file in files:
        if file.endswith(('.mp4', '.webm', '.ogg')):
            full_path = os.path.join(static_img_dir, file)
            size = os.path.getsize(full_path)
            print(f"  📹 {file}: {size:,} bytes")
else:
    print(f"\n❌ Static/img directory not found: {static_img_dir}")

# 5. Production static serving check
print(f"\n🚀 Production Static Serving:")
if not settings.DEBUG:
    print("Running in production mode")
    print(f"STATICFILES_DIRS: {getattr(settings, 'STATICFILES_DIRS', 'Not set')}")
    print(f"STATICFILES_STORAGE: {getattr(settings, 'STATICFILES_STORAGE', 'Default')}")
else:
    print("Running in development mode - Django serves static files automatically")

# 6. Create test HTML for manual testing
test_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Video Test</title>
</head>
<body>
    <h1>Video Playback Test</h1>
    <video controls width="600" height="400" style="border: 2px solid #ccc;">
        <source src="{video_url if 'video_url' in locals() else '/static/img/advertisement.mp4'}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <br><br>
    <a href="{video_url if 'video_url' in locals() else '/static/img/advertisement.mp4'}" target="_blank">Open Video Directly</a>
</body>
</html>
"""

with open('video_test.html', 'w') as f:
    f.write(test_html)

print(f"\n🧪 Created video_test.html for manual testing")
print(f"Open this file in your browser to test video playback")

print(f"\n✅ Static serving test complete!")
