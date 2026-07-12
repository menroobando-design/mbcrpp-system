from django.urls import path
from . import views

urlpatterns = [

    path("", views.report_list, name="report_list"),

    path("add/", views.add_report, name="add_report"),

    path(
        "<int:report_id>/photos/",
        views.upload_photos,
        name="upload_photos"
    ),

    path(
        "<int:report_id>/submit/",
        views.submit_report,
        name="submit_report"
    ),

    path(
        "<int:report_id>/review/",
        views.review_report,
        name="review_report"
    ),

    path(
        "<int:report_id>/approve/",
        views.approve_report,
        name="approve_report"
    ),

    path(
        "<int:report_id>/return/",
        views.return_report,
        name="return_report"
    ),

    path(
        "pending/",
        views.pending_reports,
        name="pending_reports"
    ),

    path(
        "approved/",
        views.approved_reports,
        name="approved_reports"
    ),

    path(
        "returned/",
        views.returned_reports,
        name="returned_reports"
    ),

    path(
        "<int:report_id>/",
        views.report_detail,
        name="report_detail",
    ),

    path(
        "<int:report_id>/pdf/",
        views.download_pdf,
        name="download_pdf",
    ),
]