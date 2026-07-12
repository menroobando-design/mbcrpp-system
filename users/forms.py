from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            render_value=True
        ),
        required=False
    )

    class Meta:

        model = User

        fields = [
            "username",
            "password",
            "is_active",
        ]


class UserProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        fields = [
            "role",
            "barangay",
        ]