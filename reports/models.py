from django.db import models
from barangays.models import Barangay


class WeeklyReport(models.Model):

    barangay = models.ForeignKey(Barangay, on_delete=models.CASCADE)

    report_date = models.DateField()

    waterway = models.CharField(max_length=200)

    length_covered = models.DecimalField(max_digits=8, decimal_places=2)

    waste_collected = models.DecimalField(max_digits=8, decimal_places=2)

    disposal_method = models.TextField()

    remarks = models.TextField(blank=True)

    prepared_by = models.CharField(max_length=100)

    certified_by = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.barangay} - {self.report_date}"
    

class ReportPhoto(models.Model):

    CATEGORY_CHOICES = [
        ('before', 'Before'),
        ('during', 'During'),
        ('after', 'After'),
        ('waste', 'Collected Waste'),
        ('group', 'Group Photo'),
    ]

    report = models.ForeignKey(
        WeeklyReport,
        on_delete=models.CASCADE,
        related_name='photos'
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    image = models.ImageField(upload_to='reports/')