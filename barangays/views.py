from django.shortcuts import render, redirect
from .models import Barangay
from .forms import BarangayForm


def barangay_list(request):
    barangays = Barangay.objects.all()

    return render(request, "barangays/list.html", {
        "barangays": barangays
    })


def barangay_create(request):

    if request.method == "POST":
        form = BarangayForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("barangay_list")

    else:
        form = BarangayForm()

    return render(request, "barangays/form.html", {
        "form": form
    })