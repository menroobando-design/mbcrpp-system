from django.db import models


class Barangay(models.Model):

    name = models.CharField(max_length=100, unique=True)

    municipality = models.CharField(
        max_length=100,
        default="Obando"
    )

    punong_barangay = models.CharField(max_length=100)

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