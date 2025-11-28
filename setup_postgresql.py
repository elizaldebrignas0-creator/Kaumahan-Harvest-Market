#!/usr/bin/env python
import os
import sys
import django

# Force PostgreSQL settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.production_settings')

# Override any SQLite fallback
if 'DATABASE_URL' not in os.environ:
    print("❌ ERROR: DATABASE_URL not found in environment!")
    print("Please set DATABASE_URL in Render environment variables")
    sys.exit(1)

# Parse the DATABASE_URL to ensure it's PostgreSQL
import dj_database_url
db_config = dj_database_url.parse(os.environ.get('DATABASE_URL'))

if db_config['ENGINE'] == 'django.db.backends.sqlite3':
    print("❌ ERROR: DATABASE_URL is pointing to SQLite!")
    print("DATABASE_URL should be a PostgreSQL connection string")
    print(f"Current DATABASE_URL: {os.environ.get('DATABASE_URL')}")
    sys.exit(1)

print(f"✅ PostgreSQL DATABASE_URL confirmed: {os.environ.get('DATABASE_URL')}")

django.setup()

from django.core.management import execute_from_command_line
from marketplace.models import CustomUser

def main():
    print("🔧 Running PostgreSQL migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--settings=kaumahan.production_settings'])
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
            print('✅ Admin user created in PostgreSQL')
        else:
            print('✅ Admin user already exists in PostgreSQL')
        return True
    except Exception as e:
        print(f"❌ Admin creation error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("🎉 PostgreSQL setup complete!")
    else:
        print("❌ Setup failed!")
        sys.exit(1)
