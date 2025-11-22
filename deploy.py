#!/usr/bin/env python
"""Production deployment script for Kaumahan Harvest Market"""

import os
import secrets
import subprocess
import sys

def generate_secret_key():
    """Generate a secure Django secret key"""
    return secrets.token_urlsafe(50)

def run_command(command, check=True):
    """Run shell command"""
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def main():
    print("🌾 Kaumahan Harvest Market - Production Deployment")
    print("=" * 50)
    
    # Generate new secret key
    new_secret = generate_secret_key()
    print(f"Generated new SECRET_KEY: {new_secret[:20]}...")
    
    # Update .env file
    env_content = f"""SECRET_KEY={new_secret}
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_NAME=kaumahan_db
DB_USER=your_db_user
DB_PASSWORD=your_secure_db_password
DB_HOST=127.0.0.1
DB_PORT=3306

DEFAULT_FROM_EMAIL=admin@yourdomain.com
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✓ Updated .env with production settings")
    
    # Run migrations
    if run_command("python manage.py migrate"):
        print("✓ Database migrations completed")
    
    # Collect static files
    if run_command("python manage.py collectstatic --noinput"):
        print("✓ Static files collected")
    
    print("\n🚀 Deployment preparation complete!")
    print("\nNext steps:")
    print("1. Update .env with your actual domain and database credentials")
    print("2. Set up your production database")
    print("3. Configure your web server (nginx/apache)")
    print("4. Use: gunicorn kaumahan.wsgi:application")

if __name__ == "__main__":
    main()