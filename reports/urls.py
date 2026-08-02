from django.urls import path
from . import views

urlpatterns = [

    # ==========================================
    # REPORT LIST
    # ==========================================

    path(
        "",
        views.report_list,
        name="report_list",
    ),

    path(
        "add/",
        views.add_report,
        name="add_report",
    ),

    # ==========================================
    # REPORT STATUS LISTS
    # ==========================================

    path(
        "pending/",
        views.pending_reports,
        name="pending_reports",
    ),

    path(
        "approved/",
        views.approved_reports,
        name="approved_reports",
    ),

    path(
        "returned/",
        views.returned_reports,
        name="returned_reports",
    ),

    # ==========================================
    # DCF REPORTS
    # ==========================================

    path(
        "dcf/",
        views.dcf_report_list,
        name="dcf_report_list",
    ),

    path(
        "dcf/new/",
        views.dcf_form,
        name="dcf_form",
    ),

    # ==========================================
    # MUNICIPAL REPORTS
    # ==========================================

    path(
        "municipal-report/",
        views.municipal_report,
        name="municipal_report",
    ),

    path(
        "municipal/excel/",
        views.download_municipal_excel,
        name="municipal_excel",
    ),

    # ==========================================
    # REPORT ACTIONS
    # ==========================================

    path(
        "<int:report_id>/photos/",
        views.upload_photos,
        name="upload_photos",
    ),

    path(
        "<int:report_id>/submit/",
        views.submit_report,
        name="submit_report",
    ),

    path(
        "<int:report_id>/review/",
        views.review_report,
        name="review_report",
    ),

    path(
        "<int:report_id>/approve/",
        views.approve_report,
        name="approve_report",
    ),

    path(
        "<int:report_id>/return/",
        views.return_report,
        name="return_report",
    ),

    path(
        "<int:report_id>/edit/",
        views.edit_report,
        name="edit_report",
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

    # ==========================================
    # REPORT DETAIL
    # MUST ALWAYS BE LAST
    # ==========================================

    path(
        "<int:report_id>/",
        views.report_detail,
        name="report_detail",
    ),

]