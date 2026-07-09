from django.db import models
from barangays.models import Barangay


class WeeklyReport(models.Model):

    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Submitted", "Submitted"),
        ("Approved", "Approved"),
        ("Returned", "Returned"),
    ]

    barangay = models.ForeignKey(
        Barangay,
        on_delete=models.CASCADE
    )

    week_covered = models.CharField(max_length=100)

    activity_date = models.DateField()

    activity_location = models.CharField(max_length=255)

    participants = models.PositiveIntegerField()

    waste_collected = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    waste_type = models.CharField(max_length=100)

    remarks = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Draft"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.barangay} - {self.week_covered}"


class ReportPhoto(models.Model):

    report = models.ForeignKey(
        WeeklyReport,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    image = models.ImageField(
        upload_to="weekly_reports/"
    )

    caption = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return self.caption or f"Photo {self.id}"