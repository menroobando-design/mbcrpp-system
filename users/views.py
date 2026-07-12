from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .models import UserProfile
from .forms import UserForm, UserProfileForm


# ==========================
# LOGIN
# ==========================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect("dashboard")

    return render(
        request,
        "users/login.html",
        {
            "form": form
        }
    )


# ==========================
# LOGOUT
# ==========================

@require_http_methods(["GET", "POST"])
def logout_view(request):

    logout(request)

    return redirect("login")


# ==========================
# USER LIST
# ==========================

@login_required
def user_list(request):

    profiles = UserProfile.objects.select_related(
        "user",
        "barangay"
    ).all().order_by(
        "role",
        "barangay__name"
    )

    return render(
        request,
        "users/list.html",
        {
            "profiles": profiles
        }
    )


# ==========================
# ADD USER
# ==========================

@login_required
def user_add(request):

    if not request.user.is_staff:
        return redirect("dashboard")

    if request.method == "POST":

        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save(commit=False)

            user.set_password(
                user_form.cleaned_data["password"]
            )

            user.save()

            profile = user.userprofile

            profile.role = profile_form.cleaned_data["role"]
            profile.barangay = profile_form.cleaned_data["barangay"]
            
            profile.save()

            messages.success(
                request,
                "User created successfully."
            )

            return redirect("user_list")

    else:

        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "users/add.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        }
    )


# ==========================
# EDIT USER
# ==========================

@login_required
def user_edit(request, pk):

    profile = get_object_or_404(
        UserProfile,
        pk=pk
    )

    user = profile.user

    if request.method == "POST":

        user_form = UserForm(
            request.POST,
            instance=user
        )

        profile_form = UserProfileForm(
            request.POST,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save(commit=False)

            password = user_form.cleaned_data.get("password")

            if password:
                user.set_password(password)

            user.save()

            profile_form.save()

            messages.success(
                request,
                "User updated successfully."
            )

            return redirect("user_list")

    else:

        user_form = UserForm(instance=user)

        # Don't show the hashed password
        user_form.fields["password"].initial = ""

        profile_form = UserProfileForm(
            instance=profile
        )

    return render(
        request,
        "users/edit.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "profile": profile,
        }
    )


# ==========================
# RESET PASSWORD
# ==========================

@login_required
def reset_password(request, pk):

    profile = get_object_or_404(
        UserProfile,
        pk=pk
    )

    if request.method == "POST":

        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:

            messages.error(
                request,
                "Passwords do not match."
            )

        else:

            profile.user.set_password(password)
            profile.user.save()

            messages.success(
                request,
                "Password reset successfully."
            )

            return redirect("user_list")

    return render(
        request,
        "users/reset_password.html",
        {
            "profile": profile
        }
    )