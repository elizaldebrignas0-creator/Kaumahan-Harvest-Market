#!/usr/bin/env python
import os
import sys
import django

# Set up Django without debug toolbar
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings_build')

# Remove debug toolbar from installed apps temporarily
import django.conf
if 'debug_toolbar' in django.conf.settings.INSTALLED_APPS:
    django.conf.settings.INSTALLED_APPS.remove('debug_toolbar')

django.setup()

from django.db import connection
from marketplace.models import CustomUser, Product, Category, Order, OrderItem, RatingReview, CartItem

def create_tables_manually():
    """Create database tables manually if they don't exist"""
    
    # Get all model classes
    models = [
        CustomUser, Product, Category, Order, OrderItem, RatingReview, CartItem,
        # Add Django built-in models
        django.contrib.auth.models.Permission,
        django.contrib.auth.models.Group,
        django.contrib.sessions.models.Session,
        django.contrib.admin.models.LogEntry,
        django.contrib.contenttypes.models.ContentType,
    ]
    
    with connection.schema_editor() as schema_editor:
        for model in models:
            try:
                # Check if table exists
                table_name = model._meta.db_table
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
                    if not cursor.fetchone():
                        print(f"Creating table: {table_name}")
                        schema_editor.create_model(model)
                    else:
                        print(f"Table exists: {table_name}")
            except Exception as e:
                print(f"Error creating table for {model.__name__}: {e}")

def create_admin_user():
    """Create admin user"""
    
    try:
        # Check if admin user exists
        if CustomUser.objects.filter(email='pelaezelizalde0@gmail.com').exists():
            user = CustomUser.objects.get(email='pelaezelizalde0@gmail.com')
            user.is_staff = True
            user.is_superuser = True
            user.is_approved = True
            user.save()
            print(f"✅ Updated admin: pelaezelizalde0@gmail.com")
        else:
            # Create admin user
            user = CustomUser.objects.create_superuser(
                email='pelaezelizalde0@gmail.com',
                password='admin123',
                full_name='Admin User',
                phone_number='09123456789',
                address='Admin Address'
            )
            print(f"✅ Created admin: pelaezelizalde0@gmail.com")
            
        return True
    except Exception as e:
        print(f"❌ Error creating admin: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Setting up database and admin...")
    
    # Import Django apps
    import django.contrib.auth
    import django.contrib.sessions
    import django.contrib.admin
    import django.contrib.contenttypes
    
    print("📊 Creating database tables...")
    create_tables_manually()
    
    print("👤 Creating admin user...")
    success = create_admin_user()
    
    if success:
        print("🎉 Setup complete! Admin user ready.")
        print("📧 Email: pelaezelizalde0@gmail.com")
        print("🔐 Password: admin123")
    else:
        print("❌ Setup failed!")
