from django import forms
from .models import WeeklyReport, ReportPhoto
from .widgets import MultipleFileInput


class WeeklyReportForm(forms.ModelForm):

    class Meta:

        model = WeeklyReport

        labels = {

            "biodegradable":"Biodegradable (kg)",

            "recyclable":"Recyclable (kg)",

            "residual":"Residual (kg)",

            "potential":"Potential (kg)",

            "disposal_method":"Method of Disposal",

        }

        fields = [
           "week_covered",
           "activity_date",
           "activity_location",
           "participants",
           "biodegradable",
           "recyclable",
           "residual",
           "potential",           
           "disposal_method",
           "remarks",
        ]

        widgets = {

            "activity_date": forms.DateInput(
                attrs={"type":"date"}
            ),

            "disposal_method": forms.Textarea(
                attrs={"rows":3}
            ),

            "remarks": forms.Textarea(
                attrs={"rows":3}
            ),

        }


class MultipleFileField(forms.FileField):

    widget = MultipleFileInput

    def clean(self, data, initial=None):

        if not data:
            return []

        if isinstance(data, (list, tuple)):
            return data

        return [data]


class ReportPhotoForm(forms.Form):

    category = forms.ChoiceField(
        choices=ReportPhoto.CATEGORY_CHOICES
    )

    images = MultipleFileField()

    caption = forms.CharField(
        required=False
    )