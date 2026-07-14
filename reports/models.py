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

    length_covered = models.PositiveIntegerField(
        default=0,
        help_text="Length covered in meters"
    )

    participants = models.PositiveIntegerField()

    biodegradable = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    recyclable = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    residual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    potential = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    disposal_method = models.TextField(
        blank=True
    )

    remarks = models.TextField(
        blank=True
    )

    disposal_method = models.TextField(
        verbose_name="Method of Disposal",
        blank=True
    )

    remarks = models.TextField(
        blank=True
    )

    menro_remarks = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Draft"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.barangay} - {self.week_covered}"
    
    @property
    def total_waste(self):

        return (

            self.biodegradable +

            self.recyclable +

            self.residual +

            self.potential

        )


class ReportPhoto(models.Model):

    CATEGORY_CHOICES = [

        ("Before", "Before"),

        ("During", "During"),

        ("After", "After"),

        ("Collected Waste", "Collected Waste"),

        ("Group Photo", "Group Photo"),

        ("Attendance", "Attendance"),

    ]

    report = models.ForeignKey(
        WeeklyReport,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    image = models.ImageField(
        upload_to="weekly_reports/"
    )

    caption = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):

        return f"{self.report.barangay} - {self.category}"