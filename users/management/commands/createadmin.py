from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = "Create admin user if it doesn't exist"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get("ADMIN_USERNAME", "admin")
        password = os.environ.get("ADMIN_PASSWORD", "Admin12345")
        email = os.environ.get("ADMIN_EMAIL", "admin@example.com")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS("Admin already exists."))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(self.style.SUCCESS("Admin created successfully!"))