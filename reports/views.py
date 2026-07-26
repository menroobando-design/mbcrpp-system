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

        form = WeeklyReportForm(request.POST)

        if form.is_valid():

            report = form.save(commit=False)

            report.barangay = profile.barangay

            report.status = "Draft"

            report.save()

            return redirect(
                "upload_photos",
                report.id
            )

    else:

        form = WeeklyReportForm()

    return render(
        request,
        "reports/add.html",
        {
            "form": form
        }
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

    return render(
        request,
        "reports/detail.html",
        {
            "report": report
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
            instance=report
        )

        if form.is_valid():

            report = form.save(commit=False)

            # If the report was returned,
            # automatically resubmit it.
            if report.status == "Returned":
                report.status = "Submitted"

            report.save()

            return redirect("report_detail", report.id)

    else:

        form = WeeklyReportForm(
            instance=report
        )

    return render(
        request,
        "reports/report_form.html",
        {
            "form": form,
            "edit_mode": True,
            "report": report,
        }
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

    from .generators.pdf_generator import generate_report_pdf

    pdf_file = generate_report_pdf(report)

    return FileResponse(
        open(pdf_file, "rb"),
        as_attachment=True,
        filename=f"Report_{report.id}.pdf"
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

    report = get_object_or_404(
        WeeklyReport,
        pk=report_id
    )

    # Barangay users
    if not request.user.is_staff:

        profile = get_object_or_404(
            UserProfile,
            user=request.user
        )

        # They can only delete their own reports
        if report.barangay != profile.barangay:
            return redirect("report_list")

        # Only Draft or Returned reports
        if report.status not in ["Draft", "Returned"]:
            messages.error(
                request,
                "This report can no longer be deleted."
            )
            return redirect("report_detail", report.id)

    if request.method == "POST":

        report.delete()

        messages.success(
            request,
            "Report deleted successfully."
        )

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

    if request.method == "POST":

        form = DCFReportForm(request.POST)

        if form.is_valid():

            profile = UserProfile.objects.get(user=request.user)

            report = form.save(commit=False)

            report.submitted_by = request.user

            report.barangay = profile.barangay

            report.save()

            return redirect(
                "dcf_step2",
                report.id
            )

    else:

        form = DCFReportForm()

    return render(

        request,

        "reports/dcf/step1.html",

        {

            "form": form,

        }

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

