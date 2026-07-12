from django.db import models
from django.contrib.auth.models import User
from barangays.models import Barangay
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


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
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):

        if created:
            UserProfile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):

        if hasattr(instance, "userprofile"):
            instance.userprofile.save()