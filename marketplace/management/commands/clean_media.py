from django.core.management.base import BaseCommand
from django.conf import settings
import os
from pathlib import Path


class Command(BaseCommand):
    help = 'Clean media directory of inappropriate files (logos, banners, etc.)'

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        products_dir = media_root / 'products'
        
        if not products_dir.exists():
            self.stdout.write('Products directory does not exist')
            return
        
        # Files that should not be in media/products
        inappropriate_files = [
            'logo.png', 'aboutuslogo.png', 'banner.png', 'favicon.png',
            'advertisement.mp4', 'placeholder.jpg', 'product-placeholder.jpg'
        ]
        
        removed_files = []
        for file_name in inappropriate_files:
            file_path = products_dir / file_name
            if file_path.exists():
                try:
                    os.remove(file_path)
                    removed_files.append(file_name)
                    self.stdout.write(self.style.SUCCESS(f'Removed: {file_name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to remove {file_name}: {e}'))
        
        if removed_files:
            self.stdout.write(
                self.style.SUCCESS(f'Cleaned {len(removed_files)} inappropriate files from media/products/')
            )
        else:
            self.stdout.write('No inappropriate files found in media/products/')
        
        # List remaining files
        remaining_files = list(products_dir.glob('*'))
        self.stdout.write(f'Remaining files in media/products/: {len(remaining_files)}')
        for file_path in remaining_files[:10]:  # Show first 10
            self.stdout.write(f'  - {file_path.name}')
        
        if len(remaining_files) > 10:
            self.stdout.write(f'  ... and {len(remaining_files) - 10} more files')
