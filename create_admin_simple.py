#!/usr/bin/env python
import os
import sys
import django

# Simple admin creation without debug toolbar
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings_build')

# Disable debug toolbar temporarily
if 'debug_toolbar' in sys.modules:
    del sys.modules['debug_toolbar']

django.setup()

from marketplace.models import CustomUser

def create_admin_users():
    """Create admin users if they don't exist"""
    
    admins = [
        {
            'email': 'pelaezelizalde0@gmail.com',
            'password': 'admin123',
            'full_name': 'Admin User',
            'phone_number': '09123456789',
            'address': 'Admin Address'
        },
        {
            'email': 'elizaldepelaez0@gmail.com',
            'password': 'admin123',
            'full_name': 'Super Admin',
            'phone_number': '09987654321',
            'address': 'Super Admin Address'
        }
    ]
    
    for admin_data in admins:
        email = admin_data['email']
        try:
            if CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.get(email=email)
                user.is_staff = True
                user.is_superuser = True
                user.is_approved = True
                user.save()
                print(f"✅ Updated existing admin: {email}")
            else:
                user = CustomUser.objects.create_superuser(
                    email=email,
                    password=admin_data['password'],
                    full_name=admin_data['full_name'],
                    phone_number=admin_data['phone_number'],
                    address=admin_data['address']
                )
                print(f"✅ Created new admin: {email}")
        except Exception as e:
            print(f"❌ Error with {email}: {e}")

if __name__ == "__main__":
    print("🔧 Creating admin users...")
    create_admin_users()
    print("🎉 Admin setup complete!")
