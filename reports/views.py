from django.shortcuts import render, redirect
from .models import WeeklyReport


def report_list(request):
    reports = WeeklyReport.objects.all().order_by("-created_at")

    return render(
        request,
        "reports/list.html",
        {
            "reports": reports
        }
    )


def add_report(request):
    return render(request, "reports/form.html")