from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create an initial admin (superuser) for Kaumahan Harvest Market"

    def handle(self, *args, **options):
        User = get_user_model()

        email = input("Admin email [admin@kaumahan.local]: ") or "admin@kaumahan.local"
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING("A user with that email already exists."))
            return

        password = None
        while not password:
            pwd = input("Admin password: ")
            pwd2 = input("Confirm password: ")
            if pwd != pwd2:
                self.stdout.write(self.style.ERROR("Passwords do not match. Try again."))
            elif not pwd:
                self.stdout.write(self.style.ERROR("Password cannot be empty."))
            else:
                password = pwd

        full_name = input("Admin full name [Kaumahan Admin]: ") or "Kaumahan Admin"

        user = User.objects.create_superuser(
            email=email,
            password=password,
            full_name=full_name,
            phone_number="",
            address="",
        )
        self.stdout.write(self.style.SUCCESS(f"Admin user created: {user.email}"))
