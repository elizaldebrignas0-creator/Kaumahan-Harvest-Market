#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kaumahan.settings_build')
django.setup()

from marketplace.models import CustomUser

email = "pelaezelizalde0@gmail.com"
try:
    user = CustomUser.objects.get(email=email)
    user.is_staff = True
    user.is_superuser = True
    user.is_approved = True
    user.save()
    print(f"Made {email} an admin successfully!")
except CustomUser.DoesNotExist:
    print(f"User {email} not found")
except Exception as e:
    print(f"Error: {e}")