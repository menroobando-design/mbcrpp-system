from django.db import models


class Barangay(models.Model):

    name = models.CharField(max_length=100, unique=True)

    logo = models.ImageField(
        upload_to="barangay_logos/",
        blank=True,
        null=True
    )

    committee_chair = models.CharField(
        max_length=150,
        blank=True
    )

    barangay_captain = models.CharField(
        max_length=150,
        blank=True
    )

    municipality = models.CharField(
        max_length=100,
        default="Obando"
    )
  
    environment_chair = models.CharField(max_length=100)

    contact_number = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]