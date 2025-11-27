"""
Management command to set up media directories for persistent storage
"""

from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Create and verify media directories for persistent storage'

    def handle(self, *args, **options):
        self.stdout.write('Setting up media directories...')
        
        # Create media root if it doesn't exist
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            self.stdout.write(
                self.style.SUCCESS(f'Created media root: {settings.MEDIA_ROOT}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Media root exists: {settings.MEDIA_ROOT}')
            )
        
        # Create products directory
        products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        if not os.path.exists(products_dir):
            os.makedirs(products_dir, exist_ok=True)
            self.stdout.write(
                self.style.SUCCESS(f'Created products directory: {products_dir}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Products directory exists: {products_dir}')
            )
        
        # Create business permits directory
        permits_dir = os.path.join(settings.MEDIA_ROOT, 'business_permits')
        if not os.path.exists(permits_dir):
            os.makedirs(permits_dir, exist_ok=True)
            self.stdout.write(
                self.style.SUCCESS(f'Created business permits directory: {permits_dir}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Business permits directory exists: {permits_dir}')
            )
        
        # Check permissions
        try:
            # Test write permissions
            test_file = os.path.join(settings.MEDIA_ROOT, 'test_write.tmp')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            self.stdout.write(
                self.style.SUCCESS('Media directory has proper write permissions')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Media directory write permission error: {e}')
            )
        
        # Display configuration
        self.stdout.write('\n=== Media Configuration ===')
        self.stdout.write(f'MEDIA_URL: {settings.MEDIA_URL}')
        self.stdout.write(f'MEDIA_ROOT: {settings.MEDIA_ROOT}')
        self.stdout.write(f'DEBUG: {settings.DEBUG}')
        self.stdout.write(f'DEFAULT_FILE_STORAGE: {getattr(settings, "DEFAULT_FILE_STORAGE", "Default")}')
        
        self.stdout.write(
            self.style.SUCCESS('Media directories setup complete!')
        )
