"""
Setup script for Kaumahan Harvest Market
Run this script to set up the project for the first time.
"""

import os
import sys
import subprocess

def run_command(command):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def main():
    print("=" * 60)
    print("Kaumahan Harvest Market - Setup Script")
    print("=" * 60)
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("Error: manage.py not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Create directories
    print("Creating necessary directories...")
    directories = ['media', 'media/products', 'static']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"  ✓ Created {directory}/")
        else:
            print(f"  - {directory}/ already exists")
    
    print()
    print("Setup complete!")
    print()
    print("Next steps:")
    print("1. Make sure MySQL is running and create a database named 'kaumahan_db'")
    print("2. Update database settings in kaumahan/settings.py if needed")
    print("3. Run: python manage.py makemigrations")
    print("4. Run: python manage.py migrate")
    print("5. Run: python manage.py create_admin")
    print("6. Run: python manage.py runserver")
    print()

if __name__ == '__main__':
    main()

