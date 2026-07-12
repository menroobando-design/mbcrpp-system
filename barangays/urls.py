from django.urls import path

from .views import (
    barangay_list,
    barangay_create,
    barangay_edit,
    barangay_delete,
)

urlpatterns = [
    path("", barangay_list, name="barangay_list"),

    path("add/", barangay_create, name="barangay_add"),

    path(
        "<int:pk>/edit/",
        barangay_edit,
        name="barangay_edit",
    ),

    path(
        "<int:pk>/delete/",
        barangay_delete,
        name="barangay_delete",
    ),
]