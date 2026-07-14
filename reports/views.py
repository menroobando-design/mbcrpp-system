from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import WeeklyReport, ReportPhoto
from .forms import WeeklyReportForm, ReportPhotoForm
from users.models import UserProfile
from django.http import FileResponse
from .docx_generator import generate_report_docx
from django.contrib import messages


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
