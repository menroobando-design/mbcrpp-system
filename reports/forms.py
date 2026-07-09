from django import forms
from .models import WeeklyReport, ReportPhoto


class WeeklyReportForm(forms.ModelForm):
    class Meta:
        model = WeeklyReport
        fields = [
            "barangay",
            "week_covered",
            "activity_date",
            "activity_location",
            "participants",
            "waste_collected",
            "waste_type",
            "remarks",
            "status",
        ]

        widgets = {
            "week_covered": forms.TextInput(attrs={"class": "form-control"}),
            "activity_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "activity_location": forms.TextInput(attrs={"class": "form-control"}),
            "participants": forms.NumberInput(attrs={"class": "form-control"}),
            "waste_collected": forms.NumberInput(attrs={"class": "form-control"}),
            "waste_type": forms.TextInput(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
            "barangay": forms.Select(attrs={"class": "form-control"}),
        }


class ReportPhotoForm(forms.ModelForm):
    class Meta:
        model = ReportPhoto
        fields = [
            "image",
            "caption",
        ]

        widgets = {
            "caption": forms.TextInput(
                attrs={"class": "form-control"}
            ),
        }