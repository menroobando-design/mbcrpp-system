from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from barangays.models import Barangay
from reports.models import WeeklyReport
from users.models import UserProfile
from reports.models import WeeklyReport
from django.db.models import Sum, Avg
from django.db.models.functions import TruncMonth
from django.db.models import Sum, F


@login_required
def dashboard(request):

    profile = request.user.userprofile

    # MENRO Dashboard
    if profile.role == "MENRO":

        reports = WeeklyReport.objects.all()

        context = {

            "is_menro": True,

            "total_barangays": Barangay.objects.count(),

            "total_reports": reports.count(),

            "approved_reports": reports.filter(
                status="Approved"
            ).count(),

            "submitted_reports": reports.filter(
                status="Submitted"
            ).count(),

            "returned_reports": reports.filter(
                status="Returned"
            ).count(),

            "draft_reports": reports.filter(
                status="Draft"
            ).count(),

            "recent_reports": reports.order_by(
                "-created_at"
            )[:5],

        }

    # Barangay Dashboard
    else:

        reports = WeeklyReport.objects.filter(
            barangay=profile.barangay
        )

        context = {

            "is_menro": False,

            "total_barangays": 1,

            "total_reports": reports.count(),

            "approved_reports": reports.filter(
                status="Approved"
            ).count(),

            "submitted_reports": reports.filter(
                status="Submitted"
            ).count(),

            "returned_reports": reports.filter(
                status="Returned"
            ).count(),

            "draft_reports": reports.filter(
                status="Draft"
            ).count(),

           "recent_reports": reports.order_by(
                "-created_at"
            )[:11],

        }

    return render(
        request,
        "dashboard/index.html",
        context
    )

from django.contrib.auth.decorators import login_required


@login_required
def statistics(request):

    # ==========================
    # Filter by Year
    # ==========================

    selected_year = request.GET.get("year")

    reports = WeeklyReport.objects.all()

    if selected_year:
        reports = reports.filter(
            activity_date__year=selected_year
        )

    # ==========================
    # Summary Cards
    # ==========================

    total_reports = reports.count()

    total_participants = (
        reports.aggregate(
            total=Sum("participants")
        )["total"] or 0
    )

    total_waste = sum(
        report.total_waste
        for report in reports
    )

    average_waste = (
        total_waste / total_reports
        if total_reports > 0
        else 0
    )

    # ==========================
    # Monthly Waste Collection
    # ==========================

    monthly_reports = (
        reports
        .annotate(month=TruncMonth("activity_date"))
        .values("month")
        .annotate(
            biodegradable=Sum("biodegradable"),
            recyclable=Sum("recyclable"),
            residual=Sum("residual"),
            potential=Sum("potential"),
        )
        .order_by("month")
    )

    month_labels = []
    month_totals = []

    for item in monthly_reports:

        total = (
            (item["biodegradable"] or 0)
            + (item["recyclable"] or 0)
            + (item["residual"] or 0)
            + (item["potential"] or 0)
        )

        month_labels.append(
            item["month"].strftime("%b %Y")
        )

        month_totals.append(float(total))

    # ==========================
    # Waste Composition
    # ==========================

    biodegradable = float(
        reports.aggregate(total=Sum("biodegradable"))["total"] or 0
    )

    recyclable = float(
        reports.aggregate(total=Sum("recyclable"))["total"] or 0
    )

    residual = float(
        reports.aggregate(total=Sum("residual"))["total"] or 0
    )

    potential = float(
        reports.aggregate(total=Sum("potential"))["total"] or 0
    )

    # ==========================
    # Waste Per Barangay
    # ==========================

    barangay_labels = []
    barangay_totals = []

    for barangay in Barangay.objects.all():

        barangay_reports = reports.filter(
            barangay=barangay
        )

        total = sum(
            report.total_waste
            for report in barangay_reports
        )

        barangay_labels.append(
            barangay.name
        )

        barangay_totals.append(
            float(total)
        )

    # ==========================
    # Available Years
    # ==========================

    available_years = [
        d.year
        for d in WeeklyReport.objects.dates(
            "activity_date",
            "year"
        )
    ]

    # ==========================
    # Context
    # ==========================

    context = {

        "total_reports": total_reports,

        "total_participants": total_participants,

        "total_waste": round(total_waste, 2),

        "average_waste": round(average_waste, 2),

        "month_labels": month_labels,

        "month_totals": month_totals,

        "biodegradable": biodegradable,

        "recyclable": recyclable,

        "residual": residual,

        "potential": potential,

        "barangay_labels": barangay_labels,

        "barangay_totals": barangay_totals,

        "available_years": available_years,

        "selected_year": selected_year,

    }

    return render(
        request,
        "dashboard/statistics.html",
        context
    )