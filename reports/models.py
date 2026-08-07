from django.db import models
from cloudinary.models import CloudinaryField
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

    volume_of_waste = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Total volume of waste collected (kg)"
    )

    # ======================================
    # WASTE COLLECTED (Kilograms)
    # ======================================

    biodegradable = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Biodegradable Waste (kg)"
    )

    recyclable = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Recyclable Waste (kg)"
    )

    residual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Residual Waste (kg)"
    )

    # ======================================
    # PARTICIPANTS
    # ======================================

    barangay_officials = models.PositiveIntegerField(
        default=0,
        verbose_name="No. of Barangay Officials"
    )

    sk_members = models.PositiveIntegerField(
        default=0,
        verbose_name="No. of Sangguniang Kabataan"
    )

    cso_members = models.PositiveIntegerField(
        default=0,
        verbose_name="No. of Civil Society Organization (CSO)"
    )

    participants = models.PositiveIntegerField(
        default=0,
        editable=False
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

    generated_pdf = models.FileField(
            upload_to="generated_reports/",
            blank=True,
            null=True
        )
    

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.barangay} - {self.week_covered}"

    @property
    def total_waste(self):
        return (
            self.biodegradable +
            self.recyclable +
            self.residual
        )

    def save(self, *args, **kwargs):

        self.participants = (
            self.barangay_officials +
            self.sk_members +
            self.cso_members
        )

        super().save(*args, **kwargs)


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

    image = CloudinaryField(
        "weekly_reports"
    )

    caption = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):

        return f"{self.report.barangay} - {self.category}"
    
class DCFReport(models.Model):

    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Submitted", "Submitted"),
        ("Approved", "Approved"),
        ("Returned", "Returned"),
    ]

    # ===================================================
    # GENERAL INFORMATION
    # ===================================================
    barangay = models.ForeignKey(
        Barangay,
        on_delete=models.CASCADE
    )

    month = models.CharField(max_length=30)
    year = models.PositiveIntegerField()
    week_covered = models.CharField(max_length=100, blank=True)

    submitted_by = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE
    )

    # ===================================================
    # A. BARANGAY SOLID WASTE MANAGEMENT COMMITTEE
    # ===================================================
    has_bswmc = models.BooleanField(default=False)
    bswmc_members = models.PositiveIntegerField(default=0)
    bswmc_meetings = models.PositiveIntegerField(default=0)
    has_eo = models.BooleanField(default=False)
    has_bswm_plan = models.BooleanField(default=False)

    # ===================================================
    # B. BARANGAY SOLID WASTE MANAGEMENT PROGRAM
    # ===================================================
    has_swm_program = models.BooleanField(default=False)
    swm_program_description = models.TextField(blank=True)

    # ===================================================
    # C. WEEKLY CLEAN-UP DRIVES
    # ===================================================
    cleanup_drives = models.PositiveIntegerField(default=0)
    cleanup_participants = models.PositiveIntegerField(default=0)
    cleanup_area = models.CharField(max_length=255, blank=True)

    # ===================================================
    # D. MANDATORY SEGREGATION & COLLECTION
    # ===================================================
    segregation_implemented = models.BooleanField(default=False)
    collection_schedule = models.CharField(max_length=255, blank=True)
    households_served = models.PositiveIntegerField(default=0)
    households_compliant = models.PositiveIntegerField(default=0)

    # ===================================================
    # E. MATERIALS RECOVERY FACILITY (MRF)
    # ===================================================
    has_mrf = models.BooleanField(default=False)
    mrf_location = models.CharField(max_length=255, blank=True)
    mrf_operational = models.BooleanField(default=False)
    mrf_workers = models.PositiveIntegerField(default=0)

    # ===================================================
    # F. WASTE DIVERSION
    # ===================================================
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
        default=0,
        verbose_name="Residual w/ Potential (kg)"
    )

    # ===================================================
    # G. ENFORCEMENT
    # ===================================================
    has_ordinance = models.BooleanField(default=False)
    violations_recorded = models.PositiveIntegerField(default=0)
    penalties_imposed = models.PositiveIntegerField(default=0)

    # ===================================================
    # H. IEC CAMPAIGN & BEST PRACTICES
    # ===================================================
    iec_activities = models.PositiveIntegerField(default=0)
    iec_participants = models.PositiveIntegerField(default=0)
    best_practices = models.TextField(blank=True)

    # ===================================================
    # CERTIFICATION
    # ===================================================
    prepared_by = models.CharField(max_length=150, blank=True)
    certified_by = models.CharField(max_length=150, blank=True)

    # ===================================================
    # SYSTEM FIELDS
    # ===================================================
    menro_remarks = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Draft"
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    returned_at = models.DateTimeField(
        null=True,
        blank=True
    )

    submitted_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="submitted_reports"
    )

    reviewed_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_reports"
    )

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.barangay} - {self.month} {self.year}"

    @property
    def total_waste(self):
        return (
            self.biodegradable +
            self.recyclable +
            self.residual             
        )   


    