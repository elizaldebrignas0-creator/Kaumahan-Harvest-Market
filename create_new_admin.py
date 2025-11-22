#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.production_settings')
django.setup()

from marketplace.models import CustomUser

email = "pelaezelizalde0@gmail.com"
if CustomUser.objects.filter(email=email).exists():
    print(f"User {email} already exists")
else:
    user = CustomUser.objects.create_superuser(
        email=email,
        password="admin123",
        full_name="Admin User",
        phone_number="09123456789",
        address="Admin Address"
    )
    print(f"Created new admin user: {user.email}")