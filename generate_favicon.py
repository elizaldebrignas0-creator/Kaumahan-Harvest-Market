from PIL import Image
import os

def generate_favicon(input_path, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Open the original image
    try:
        img = Image.open(input_path)
        
        # Create favicon.ico (must be exactly 32x32 for .ico format)
        ico_sizes = [(16, 16), (32, 32), (48, 48)]
        ico_img = img.resize((32, 32), Image.Resampling.LANCZOS)
        ico_img.save(os.path.join(output_dir, 'favicon.ico'), sizes=ico_sizes)
        
        # Create PNG versions
        sizes = [16, 32, 180]  # Standard favicon sizes
        for size in sizes:
            resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
            if size == 180:
                resized_img.save(os.path.join(output_dir, 'apple-touch-icon.png'))
            else:
                resized_img.save(os.path.join(output_dir, f'favicon-{size}x{size}.png'))
                
        print("Favicon files generated successfully!")
        return True
        
    except Exception as e:
        print(f"Error generating favicon: {e}")
        return False

if __name__ == "__main__":
    # Path to your original image
    input_image = os.path.join('static', 'img', 'favicon_original.png')
    output_directory = os.path.join('static', 'img')
    
    generate_favicon(input_image, output_directory)
