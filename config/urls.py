from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

from dashboard.views import dashboard
from dashboard.views import dashboard, statistics

urlpatterns = [

    path("admin/", admin.site.urls),

    path(
        "",
        dashboard,
        name="dashboard"
    ),

    path(
        "statistics/",
        statistics,
        name="statistics"
    ),

    path(
        "",
        include("users.urls")
    ),

    path(
        "barangays/",
        include("barangays.urls")
    ),

    path(
        "reports/",
        include("reports.urls")
    ),

   
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )