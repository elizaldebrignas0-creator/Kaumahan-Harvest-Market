import os
import subprocess

print("=== VIDEO FILE ANALYSIS ===")

video_path = "static/img/advertisement.mp4"

if os.path.exists(video_path):
    size = os.path.getsize(video_path)
    print(f"✅ Video file exists: {size:,} bytes ({size/1024/1024:.2f} MB)")
    
    # Try to get video info using ffprobe if available
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'error', '-show_format', '-show_streams', 
            video_path
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Video file format information:")
            print(result.stdout)
        else:
            print("⚠️  Could not analyze video format")
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("⚠️  ffprobe not available - cannot analyze video format")
    
    # Check file header to see if it's a valid MP4
    with open(video_path, 'rb') as f:
        header = f.read(12)
        print(f"File header: {header.hex()}")
        
        # Check for MP4 signature
        if header.startswith(b'ftyp'):
            print("✅ Valid MP4 file signature")
        else:
            print("❌ Invalid MP4 file signature")
            
else:
    print(f"❌ Video file not found: {video_path}")

print("\n=== RECOMMENDATIONS ===")
print("1. If video file is invalid, re-encode it:")
print("   ffmpeg -i input.mp4 -c:v libx264 -c:a aac -strict experimental output.mp4")
print("2. Try different video formats (webm, ogg)")
print("3. Ensure video is not corrupted")
print("4. Check browser console for specific error messages")
