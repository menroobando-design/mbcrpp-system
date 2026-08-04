from django.contrib import admin
from .models import Barangay


@admin.register(Barangay)
class BarangayAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "barangay_captain",
        "committee_chair",
        "active",
    )

    search_fields = (
        "name",
        "barangay_captain",
        "committee_chair",
    )

    list_filter = (
        "active",
    )

    ordering = (
        "name",
    )

    fields = (
        "name",
        "municipality",
        "logo",

        "barangay_captain",
        "captain_signature",

        "committee_chair",
        "committee_signature",

        "contact_number",
        "email",
        "active",
    )