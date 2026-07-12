from django.shortcuts import render, redirect, get_object_or_404

from .models import Barangay
from .forms import BarangayForm


def barangay_list(request):

    barangays = Barangay.objects.all()

    return render(
        request,
        "barangays/list.html",
        {
            "barangays": barangays
        }
    )


def barangay_create(request):

    if request.method == "POST":

        form = BarangayForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("barangay_list")

    else:

        form = BarangayForm()

    return render(
        request,
        "barangays/form.html",
        {
            "form": form
        }
    )


def barangay_edit(request, pk):

    barangay = get_object_or_404(
        Barangay,
        pk=pk
    )

    if request.method == "POST":

        form = BarangayForm(
            request.POST,
            request.FILES,
            instance=barangay
        )

        if form.is_valid():

            form.save()

            return redirect("barangay_list")

    else:

        form = BarangayForm(
            instance=barangay
        )

    return render(
        request,
        "barangays/form.html",
        {
            "form": form,
            "edit_mode": True,
        }
    )


def barangay_delete(request, pk):

    barangay = get_object_or_404(
        Barangay,
        pk=pk
    )

    if request.method == "POST":

        barangay.delete()

        return redirect("barangay_list")

    return render(
        request,
        "barangays/delete.html",
        {
            "barangay": barangay
        }
    )