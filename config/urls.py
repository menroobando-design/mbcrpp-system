from django.contrib import admin
from django.urls import path, include
from dashboard.views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", dashboard),

    path("barangays/", include("barangays.urls")),

    path("reports/", include("reports.urls")),
]