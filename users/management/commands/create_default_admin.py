from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Creates the default admin user"

    def handle(self, *args, **kwargs):

        username = "admin"

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS("Admin already exists.")
            )
            return

        User.objects.create_superuser(
            username="admin",
            email="admin@obando.gov.ph",
            password="Admin12345"
        )

        self.stdout.write(
            self.style.SUCCESS("Default admin created.")
        )