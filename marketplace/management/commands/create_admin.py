from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create an initial admin (superuser) for Kaumahan Harvest Market"

    def handle(self, *args, **options):
        User = get_user_model()

        email = "elizaldepelaez0@gmail.com"
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING("Admin user already exists."))
            return

        password = "admin123"
        full_name = "Kaumahan Admin"

        user = User.objects.create_superuser(
            email=email,
            password=password,
            full_name=full_name,
            phone_number="09123456789",
            address="Admin Address",
        )
        self.stdout.write(self.style.SUCCESS(f"Admin user created: {user.email}"))
