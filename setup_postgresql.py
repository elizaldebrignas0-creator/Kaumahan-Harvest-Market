#!/usr/bin/env python
import os
import sys
import django

# Force PostgreSQL settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.production_settings')

# Parse the DATABASE_URL to check database type
import dj_database_url
db_config = dj_database_url.parse(os.environ.get('DATABASE_URL', ''))

print(f"🔍 Current DATABASE_URL: {os.environ.get('DATABASE_URL', 'NOT SET')}")

if db_config['ENGINE'] == 'django.db.backends.sqlite3':
    print("⚠️ WARNING: DATABASE_URL is pointing to SQLite!")
    print("📝 This will cause data loss after deployments!")
    print("🔧 To fix: Set DATABASE_URL to PostgreSQL in Render dashboard")
    print("📋 Continuing with SQLite setup for now...\n")
    
    # Use SQLite settings temporarily
    os.environ['DJANGO_SETTINGS_MODULE'] = 'kaumahan.settings_build'
    print("🔄 Switched to build settings for SQLite setup")

django.setup()

from django.core.management import execute_from_command_line
from marketplace.models import CustomUser

def main():
    print("🔧 Running database migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed successfully")
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False
    
    print("👤 Creating admin user...")
    try:
        if not CustomUser.objects.filter(email='pelaezelizalde0@gmail.com').exists():
            CustomUser.objects.create_superuser(
                email='pelaezelizalde0@gmail.com',
                password='admin123',
                full_name='Admin User',
                phone_number='09123456789',
                address='Admin Address'
            )
            print('✅ Admin user created')
        else:
            print('✅ Admin user already exists')
        return True
    except Exception as e:
        print(f"❌ Admin creation error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("🎉 Database setup complete!")
        print("⚠️  WARNING: Still using SQLite - fix DATABASE_URL in Render!")
    else:
        print("❌ Setup failed!")
        sys.exit(1)
