from django.urls import path
from .views import barangay_list, barangay_create

urlpatterns = [
    path("", barangay_list, name="barangay_list"),
    path("add/", barangay_create, name="barangay_add"),
]