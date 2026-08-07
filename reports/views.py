from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    WeeklyReport,
    ReportPhoto,
    DCFReport,
)

from .forms import (
    WeeklyReportForm,
    ReportPhotoForm,
    DCFReportForm,
    DCFStep2Form,
    DCFStep3Form,
    DCFStep4Form,
)

from users.models import UserProfile
from django.http import FileResponse
from .docx_generator import generate_report_docx
from django.contrib import messages
from django.utils import timezone
import cloudinary.uploader
from django.http import HttpResponse
from openpyxl import load_workbook
from pathlib import Path

from django.core.files import File
from django.core.files.base import ContentFile
from .generators.pdf_generator import generate_report_pdf
from django.core.files import File
import os

from io import BytesIO
from reports.generators.municipal_excel import generate_municipal_excel


@login_required
def report_list(request):

    if request.user.is_staff:

        reports = WeeklyReport.objects.all().order_by("-created_at")

    else:

        profile = get_object_or_404(
            UserProfile,
            user=request.user
        )

        reports = WeeklyReport.objects.filter(
            barangay=profile.barangay
        ).order_by("-created_at")

    return render(
        request,
        "reports/list.html",
        {
            "reports": reports
        }
    )


@login_required
def add_report(request):

    if request.user.is_staff:
        return redirect("report_list")

    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if request.method == "POST":

        form = WeeklyReportForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            report = form.save(commit=False)

            report.barangay = profile.barangay
            report.status = "Draft"
            report.save()

            # Save uploaded photos
            photo_fields = {
                "Before": "before_photos",
                "During": "during_photos",
                "After": "after_photos",
                "Collected Waste": "waste_photos",
                "Group Photo": "group_photos",
                "Attendance": "attendance_photos",
            }

            for category, field_name in photo_fields.items():

                for image in request.FILES.getlist(field_name):

                    ReportPhoto.objects.create(
                        report=report,
                        category=category,
                        image=image,
                    )

            messages.success(
                request,
                "Report saved successfully."
            )

            return redirect("report_list")

    else:

        form = WeeklyReportForm()

    return render(
        request,
        "reports/add.html",
        {
            "form": form,
            "photo_categories": ReportPhoto.CATEGORY_CHOICES,
        },
    )


@login_required
def upload_photos(request, report_id):

    report = get_object_or_404(
        WeeklyReport,
        pk=report_id
    )

    if not request.user.is_staff:

        profile = UserProfile.objects.get(user=request.user)

        if report.barangay != profile.barangay:

            return redirect("report_list")

    if request.method == "POST":

        form = ReportPhotoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            category = form.cleaned_data["category"]

            caption = form.cleaned_data["caption"]

            images = request.FILES.getlist("images")

            for image in images:

                ReportPhoto.objects.create(

                    report=report,

                    category=category,

                    image=image,

                    caption=caption,

                )

            return redirect(
               "upload_photos",
                report.id
            )

    else:

        form = ReportPhotoForm()

    return render(
        request,
        "reports/upload_photos.html",
        {
            "report": report,
            "form": form,
            "photos": report.photos.all(),
        }
    )


@login_required
def submit_report(request, report_id):

    report = get_object_or_404(
        WeeklyReport,
        pk=report_id
    )

    if not request.user.is_staff:

        profile = UserProfile.objects.get(user=request.user)

        if report.barangay != profile.barangay:
            return redirect("report_list")

    # -----------------------------------
    # Generate PDF BEFORE submitting
    # -----------------------------------

    pdf_path = generate_report_pdf(report)

    with open(pdf_path, "rb") as pdf:

        report.generated_pdf.save(
            f"Report_{report.id}.pdf",
            File(pdf),
            save=False,
        )

    os.remove(pdf_path)

    # -----------------------------------
    # Submit report
    # -----------------------------------

    report.status = "Submitted"

    report.submitted_at = timezone.now()

    report.submitted_by = request.user

    report.save()

    return redirect("report_list")


@login_required
def review_report(request, report_id):

    if not request.user.is_staff:

        return redirect("report_list")

    report = get_object_or_404(
        WeeklyReport,
        pk=report_id
    )

    return render(
        request,
        "reports/review.html",
        {
            "report": report
        }
    )


@login_required
def approve_report(request, report_id):

    if not request.user.is_staff:

        return redirect("report_list")

    report = get_object_or_404(
        WeeklyReport,
        pk=report_id
    )

    report.status = "Approved"

    report.approved_at = timezone.now()

    report.reviewed_by = request.user

    report.save()

    return redirect("report_list")


@login_required
def return_report(request, report_id):

    if not request.user.is_staff:
        return redirect("report_list")

    report = get_object_or_404(
        WeeklyReport,
        pk=report_id
    )

    if request.method == "POST":

        report.status = "Returned"

        report.returned_at = timezone.now()

        report.reviewed_by = request.user

        report.menro_remarks = request.POST.get(
            "menro_remarks",
            ""
        )

        report.save()

        return redirect("report_list")

    return render(
        request,
        "reports/return.html",
        {
            "report": report
        }
    )


@login_required
def approved_reports(request):

    reports = WeeklyReport.objects.filter(
        status="Approved"
    ).order_by("-created_at")

    return render(
        request,
        "reports/approved_reports.html",
        {
            "reports": reports
        }
    )


@login_required
def report_detail(request, report_id):

    report = get_object_or_404(
        WeeklyReport,
        pk=report_id
    )

    # Barangay users can only view their own reports
    if not request.user.is_staff:

        profile = get_object_or_404(
            UserProfile,
            user=request.user
        )

        if report.barangay != profile.barangay:
            return redirect("report_list")

    profile = UserProfile.objects.get(user=request.user)

    return render(
        request,
        "reports/detail.html",
        {
            "report": report,
            "profile": profile,
        }
    )


@login_required
def edit_report(request, report_id):

    report = get_object_or_404(
        WeeklyReport,
        pk=report_id
    )

    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    # Only the owner can edit
    if report.barangay != profile.barangay:
        return redirect("report_list")

    # Only Draft and Returned reports are editable
    if report.status not in ["Draft", "Returned"]:
        return redirect("report_detail", report.id)

    if request.method == "POST":

        form = WeeklyReportForm(
            request.POST,
            request.FILES,
            instance=report
        )

        if form.is_valid():

            report = form.save(commit=False)

            # If the report was returned,
            # automatically resubmit it.
            if report.status == "Returned":
                report.status = "Submitted"

            report.save()

            photo_fields = {
                "before_photos": "Before",
                "during_photos": "During",
                "after_photos": "After",
                "waste_photos": "Collected Waste",
                "group_photos": "Group Photo",
                "attendance_photos": "Attendance",
            }

            for field_name, category in photo_fields.items():

                for image in request.FILES.getlist(field_name):

                    ReportPhoto.objects.create(
                        report=report,
                        category=category,
                        image=image,
                    )

            return redirect("report_detail", report.id)

    else:

        form = WeeklyReportForm(
            instance=report
        )

    return render(
        request,
        "reports/add.html",
        {
            "form": form,
            "report": report,
            "photos": report.photos.all(),
        }
    )

@login_required
def delete_photo(request, photo_id):

    photo = get_object_or_404(
        ReportPhoto,
        pk=photo_id
    )

    report = photo.report

    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if profile.role != "MENRO":

        if report.barangay != profile.barangay:
            return redirect("report_list")

    if photo.image:

        try:
            cloudinary.uploader.destroy(photo.image.public_id)
        except Exception:
            pass

    photo.delete()

    messages.success(
        request,
        "Photo deleted successfully."
    )

    return redirect(
        "edit_report",
        report.id
    )


from django.http import FileResponse


@login_required
def download_pdf(request, report_id):

    report = get_object_or_404(
        WeeklyReport,
        pk=report_id
    )

    if not request.user.is_staff:

        profile = get_object_or_404(
            UserProfile,
            user=request.user
        )

        if report.barangay != profile.barangay:
            return redirect("report_list")

    # -------------------------------------
    # Download existing PDF only
    # -------------------------------------

    if report.generated_pdf:

        return FileResponse(
            report.generated_pdf.open("rb"),
            as_attachment=True,
            filename=f"Report_{report.id}.pdf"
        )

    return HttpResponse(
        "PDF has not been generated yet.",
        status=404
    )

@login_required
def pending_reports(request):

    if not request.user.is_staff:
        return redirect("report_list")

    reports = WeeklyReport.objects.filter(
        status="Submitted"
    ).order_by("-created_at")

    return render(
        request,
        "reports/pending_reports.html",
        {
            "reports": reports
        }
    )


@login_required
def returned_reports(request):

    if not request.user.is_staff:
        return redirect("report_list")

    reports = WeeklyReport.objects.filter(
        status="Returned"
    ).order_by("-created_at")

    return render(
        request,
        "reports/returned_reports.html",
        {
            "reports": reports
        }
    )


@login_required
def delete_report(request, report_id):

    print(">>> DELETE REPORT VIEW OPENED <<<")

    report = get_object_or_404(
        WeeklyReport,
        pk=report_id
    )

    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    # ----------------------------------------
    # MENRO Admin / Staff
    # Can delete ANY report
    # ----------------------------------------

    if profile.role == "MENRO":
        pass

    # ----------------------------------------
    # Barangay Users
    # ----------------------------------------

    else:

        # Can only delete their own reports
        if report.barangay != profile.barangay:
            return redirect("report_list")

        # Can only delete Draft or Returned reports
        if report.status not in ["Draft", "Returned"]:

            messages.error(
                request,
                "This report can no longer be deleted."
            )

            return redirect(
                "report_detail",
                report.id
            )

    # ----------------------------------------
    # Delete Report
    # ----------------------------------------

    if request.method == "POST":

        # ---------------------------------------
        # Delete all uploaded images first
        # ---------------------------------------

        for photo in report.photos.all():

            try:

                if photo.image:

                    cloudinary.uploader.destroy(
                        photo.image.public_id
                    )

            except Exception as e:

                print("Cloudinary delete error:", e)

        # ---------------------------------------
        # Delete database records
        # ---------------------------------------

        report.photos.all().delete()

        report.delete()

        messages.success(
            request,
            "Report deleted successfully."
        )

        # MENRO goes back to Approved Reports
        if profile.role == "MENRO":
            return redirect("approved_reports")

        # Barangay users go back to their reports
        return redirect("report_list")

    return render(
        request,
        "reports/delete_report.html",
        {
            "report": report
        }
    )


# ==========================================
# DCF REPORT LIST
# ==========================================

@login_required
def dcf_report_list(request):

    if request.user.is_staff:

        reports = DCFReport.objects.all().order_by("-created_at")

    else:

        reports = DCFReport.objects.filter(
            submitted_by=request.user
        ).order_by("-created_at")

    return render(

        request,

        "reports/dcf/list.html",

        {

            "reports": reports,

        }

    )



# ==========================================
# DCF REPORTS
# ==========================================

@login_required
def dcf_step1(request):

    if request.user.is_staff:
        return redirect("dcf_report_list")

    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if request.method == "POST":

        form = DCFReportForm(request.POST)

        if form.is_valid():

            report = form.save(commit=False)

            report.barangay = profile.barangay
            report.submitted_by = request.user
            report.status = "Draft"

            report.save()

            messages.success(
                request,
                "DCF Report saved successfully."
            )

            return redirect("dcf_report_list")

    else:

        form = DCFReportForm()

    return render(
        request,
        "reports/dcf_form.html",
        {
            "form": form
        },
    )

@login_required
def dcf_step2(request, report_id):

    report = get_object_or_404(
        DCFReport,
        pk=report_id
    )

    if request.method == "POST":

        form = DCFStep2Form(
            request.POST,
            instance=report
        )

        if form.is_valid():

            form.save()

            return redirect(
                "dcf_step3",
                report.id
            )

    else:

        form = DCFStep2Form(
            instance=report
        )

    return render(

        request,

        "reports/dcf/step2.html",

        {

            "form": form,

            "report": report,

        }

    )


@login_required
def dcf_step3(request, report_id):

    report = get_object_or_404(
        DCFReport,
        pk=report_id
    )

    if request.method == "POST":

        form = DCFStep3Form(
            request.POST,
            instance=report
        )

        if form.is_valid():

            form.save()

            return redirect(
                "dcf_step4",
                report.id
            )

    else:

        form = DCFStep3Form(
            instance=report
        )

    return render(

        request,

        "reports/dcf/step3.html",

        {

            "form": form,

            "report": report,

        }

    )


@login_required
def dcf_step4(request, report_id):

    report = get_object_or_404(
        DCFReport,
        pk=report_id
    )

    if request.method == "POST":

        form = DCFStep4Form(
            request.POST,
            instance=report
        )

        if form.is_valid():

            form.save()

            return redirect(
                "dcf_step5",
                report.id
            )

    else:

        form = DCFStep4Form(
            instance=report
        )

    return render(

        request,

        "reports/dcf/step4.html",

        {

            "form": form,

            "report": report,

        }

    )



@login_required
def dcf_form(request):

    if request.user.is_staff:
        return redirect("dcf_report_list")

    profile = get_object_or_404(
        UserProfile,
        user=request.user
    )

    if request.method == "POST":

        form = DCFReportForm(request.POST)

        if form.is_valid():

            report = form.save(commit=False)

            report.barangay = profile.barangay
            report.submitted_by = request.user
            report.status = "Draft"

            report.save()

            messages.success(
                request,
                "DCF Report saved successfully."
            )

            return redirect("dcf_report_list")

    else:

        form = DCFReportForm()

    return render(
        request,
        "reports/dcf/form.html",
        {
            "form": form,
        },
    )


# ==========================================
# MUNICIPAL WEEKLY REPORT
# ==========================================

@login_required
def municipal_report(request):

    reports = WeeklyReport.objects.filter(
        status="Approved"
    )

    month = request.GET.get("month")
    year = request.GET.get("year")
    week = request.GET.get("week")

    if month:
        reports = reports.filter(activity_date__month=month)

    if year:
        reports = reports.filter(activity_date__year=year)

    if week:
        reports = reports.filter(week_covered=week)

    reports = reports.order_by("barangay__name")

    return render(
        request,
        "reports/municipal_report.html",
        {
            "reports": reports,
            "selected_month": month,
            "selected_year": year,
            "selected_week": week,
        },
    )


@login_required
def download_municipal_excel(request):

    template_path = (
        Path(__file__).resolve().parent
        / "templates_excel"
        / "municipal_template.xlsx"
    )

    workbook = load_workbook(template_path)

    worksheet = workbook.active

    reports = WeeklyReport.objects.filter(
        status="Approved"
    ).order_by("barangay__name")

    row = 7

    for report in reports:

        worksheet[f"B{row}"] = report.barangay.municipality.name
        worksheet[f"C{row}"] = report.barangay.name

        # Conducted Clean-up
        worksheet[f"D{row}"] = 1
        worksheet[f"E{row}"] = 0

        # Participants
        worksheet[f"F{row}"] = report.participants

        # Posted in Social Media
        worksheet[f"G{row}"] = ""
        worksheet[f"H{row}"] = ""

        # Activity
        worksheet[f"I{row}"] = report.activity_location
        worksheet[f"J{row}"] = report.length_covered

        # Waste
        worksheet[f"K{row}"] = report.total_waste

        # Disposal
        worksheet[f"L{row}"] = report.disposal_method

        # Remarks
        worksheet[f"M{row}"] = report.remarks

        row += 1

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="Municipal_Weekly_Report.xlsx"'
    )

    workbook.save(response)

    return response


@login_required
def download_kalinisan_excel(request):

    workbook, sheet = generate_municipal_excel()

    output = BytesIO()

    workbook.save(output)

    output.seek(0)

    response = HttpResponse(
        output.read(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        'attachment; filename="Kalinisan_Weekly_Report.xlsx"'
    )

    return response


