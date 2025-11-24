from django.core.management.base import BaseCommand
from django.conf import settings
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Setup media directories and ensure proper permissions'

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        
        # Create main media directory
        media_root.mkdir(parents=True, exist_ok=True)
        self.stdout.write(f"Created media directory: {media_root}")

        # Create subdirectories
        subdirs = ['products', 'business_permits', 'avatars', 'temp']
        
        for subdir in subdirs:
            dir_path = media_root / subdir
            dir_path.mkdir(exist_ok=True)
            self.stdout.write(f"Created subdirectory: {dir_path}")

        # Create placeholder files if they don't exist
        placeholder_path = media_root / 'products' / 'placeholder.jpg'
        if not placeholder_path.exists():
            # Copy from static placeholder
            static_placeholder = Path(settings.STATIC_ROOT) / 'img' / 'product-placeholder.jpg'
            if static_placeholder.exists():
                import shutil
                shutil.copy2(static_placeholder, placeholder_path)
                self.stdout.write(f"Created placeholder: {placeholder_path}")
            else:
                # Create a simple placeholder
                try:
                    from PIL import Image, ImageDraw
                    img = Image.new('RGB', (300, 300), color='#f8f9fa')
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([50, 50, 250, 250], outline='#dee2e6', width=2)
                    draw.text((100, 140), "No Image", fill='#6c757d')
                    img.save(placeholder_path)
                    self.stdout.write(f"Generated placeholder: {placeholder_path}")
                except ImportError:
                    self.stdout.write(
                        self.style.WARNING('PIL not available, please install it to generate placeholders')
                    )

        # Check permissions
        try:
            os.chmod(media_root, 0o755)
            for subdir in subdirs:
                dir_path = media_root / subdir
                os.chmod(dir_path, 0o755)
            self.stdout.write(self.style.SUCCESS('Set directory permissions'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not set permissions: {e}'))

        # Verify media URL configuration
        self.stdout.write(f"Media URL: {settings.MEDIA_URL}")
        self.stdout.write(f"Media Root: {settings.MEDIA_ROOT}")
        self.stdout.write(f"Static URL: {settings.STATIC_URL}")
        self.stdout.write(f"Static Root: {settings.STATIC_ROOT}")

        self.stdout.write(self.style.SUCCESS('Media setup completed successfully!'))
