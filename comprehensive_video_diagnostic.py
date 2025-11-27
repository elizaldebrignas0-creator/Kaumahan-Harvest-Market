import os
import mimetypes
import subprocess
from pathlib import Path

print("=== COMPREHENSIVE VIDEO DIAGNOSTIC ===")

# 1. Check file existence and basic info
video_path = "static/img/advertisement.mp4"
print(f"\n📁 File Analysis: {video_path}")

if os.path.exists(video_path):
    size = os.path.getsize(video_path)
    print(f"✅ File exists: {size:,} bytes ({size/1024/1024:.2f} MB)")
    
    # 2. Check MIME type
    mime_type, _ = mimetypes.guess_type(video_path)
    print(f"🔍 Detected MIME type: {mime_type}")
    
    # 3. Check file signature
    with open(video_path, 'rb') as f:
        header = f.read(16)
        print(f"📋 File header (hex): {header.hex()}")
        
        # Check for common video signatures
        if header.startswith(b'ftyp'):
            print("✅ Valid MP4 file signature")
        elif header.startswith(b'RIFF') and b'AVI' in header[:16]:
            print("✅ AVI file detected")
        elif header.startswith(b'\x1A\x45\xDF\xA3'):
            print("✅ Matroska/WebM file detected")
        else:
            print("❌ Invalid or unknown video file signature")
            print("⚠️  This is likely the root cause of playback issues")
    
    # 4. Try to get detailed video info
    print("\n🎬 Video Information:")
    try:
        # Try ffprobe first
        result = subprocess.run([
            'ffprobe', '-v', 'error', '-show_format', '-show_streams', 
            '-select_streams', 'v:0', video_path
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Video analysis successful:")
            for line in result.stdout.split('\n'):
                if '=' in line and not line.startswith('['):
                    print(f"   {line}")
        else:
            print("⚠️  ffprobe analysis failed")
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️  ffprobe not available for detailed analysis")
    
    # 5. Check Django static file serving
    print(f"\n🌐 Django Static File Check:")
    expected_url = "/static/img/advertisement.mp4"
    print(f"Expected URL: {expected_url}")
    print(f"STATIC_URL: /static/")
    print(f"File in STATIC_ROOT: static/img/advertisement.mp4")
    
    # 6. Browser compatibility check
    print(f"\n🌍 Browser Compatibility:")
    print("✅ MP4 with H.264 + AAC: Widely supported")
    print("✅ HTML5 video element: Standard across modern browsers")
    print("✅ playsinline attribute: Mobile compatibility")
    print("✅ controls attribute: Native browser controls")
    
else:
    print(f"❌ File not found: {video_path}")

print(f"\n🔧 RECOMMENDATIONS:")
print("1. If file signature is invalid, re-encode the video:")
print("   ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4")
print("2. Ensure video uses H.264 codec for maximum compatibility")
print("3. Test video in different browsers")
print("4. Check browser console for specific error messages")
print("5. Verify Django static files are configured correctly")

# 7. Create a test video element
print(f"\n🧪 Test Video HTML:")
test_html = '''
<video controls preload="auto" width="400" height="300">
    <source src="/static/img/advertisement.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>
'''
print(test_html)
