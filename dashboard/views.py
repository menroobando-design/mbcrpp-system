from django.shortcuts import render
from barangays.models import Barangay


def dashboard(request):

    total_barangays = Barangay.objects.count()

    context = {
        "total_barangays": total_barangays,
        "total_reports": 0,
        "waste_collected": 0,
        "pending_reports": 0,
    }

    return render(request, "dashboard/index.html", context)