from django.contrib import admin
from .models import Barangay


@admin.register(Barangay)
class BarangayAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "punong_barangay",
        "environment_chair",
        "contact_number",
        "active",
    )

    search_fields = (
        "name",
        "punong_barangay",
    )

    list_filter = (
        "active",
    )

    ordering = (
        "name",
    )