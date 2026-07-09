from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "barangay",
        "contact_number",
    )

    list_filter = (
        "role",
        "barangay",
    )

    search_fields = (
        "user__username",
        "barangay__name",
    )