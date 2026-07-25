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

    
    path(
        "<int:report_id>/delete/",
        views.delete_report,
        name="delete_report",
    ),

    path(
        "dcf/",
        views.dcf_report_list,
        name="dcf_report_list",
    ),

    path(
        "dcf/new/",
        views.dcf_step1,
        name="dcf_step1",
    ),

    path(
        "dcf/<int:report_id>/step2/",
        views.dcf_step2,
        name="dcf_step2"
    ),

    path(
        "dcf/<int:report_id>/step3/",
        views.dcf_step3,
        name="dcf_step3"
    ),
    
    path(
        "dcf/<int:report_id>/step4/",
        views.dcf_step4,
        name="dcf_step4",
    ),

]