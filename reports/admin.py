from django.contrib import admin
from .models import (
    WeeklyReport,
    ReportPhoto,
    DCFReport,
)

admin.site.register(WeeklyReport)
admin.site.register(ReportPhoto)
admin.site.register(DCFReport)