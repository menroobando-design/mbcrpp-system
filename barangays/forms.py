from django import forms
from .models import Barangay


class BarangayForm(forms.ModelForm):

    class Meta:

        model = Barangay

        fields = [

            "name",

            "logo",

            "barangay_captain",

            "committee_chair",

            "environment_chair",

            "contact_number",

            "email",

            "active",

        ]

        widgets = {

            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "barangay_captain": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "committee_chair": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "environment_chair": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "contact_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),

            "active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),

        }