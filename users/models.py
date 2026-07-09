from django.db import models
from django.contrib.auth.models import User
from barangays.models import Barangay


class UserProfile(models.Model):

    ROLE_CHOICES = [
        ("MENRO", "MENRO"),
        ("BARANGAY", "Barangay"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="BARANGAY"
    )

    barangay = models.ForeignKey(
        Barangay,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    contact_number = models.CharField(
        max_length=30,
        blank=True
    )

    def __str__(self):
        if self.role == "MENRO":
            return f"{self.user.username} (MENRO)"

        return f"{self.user.username} - {self.barangay}"