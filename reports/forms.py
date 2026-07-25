from django import forms
from .widgets import MultipleFileInput
from .models import (
    WeeklyReport,
    ReportPhoto,
    DCFReport,
)


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
           "length_covered",
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


# =====================================================
# DCF REPORT - STEP 1
# =====================================================

class DCFReportForm(forms.ModelForm):

    class Meta:

        model = DCFReport

        fields = [

            "month",

            "year",

            "week_covered",

            "prepared_by",

        ]

        widgets = {

            "month": forms.Select(

                choices=[

                    ("January","January"),
                    ("February","February"),
                    ("March","March"),
                    ("April","April"),
                    ("May","May"),
                    ("June","June"),
                    ("July","July"),
                    ("August","August"),
                    ("September","September"),
                    ("October","October"),
                    ("November","November"),
                    ("December","December"),

                ]

            ),

            "year": forms.NumberInput(

                attrs={

                    "min":2024,

                    "max":2100,

                }

            ),

            "week_covered": forms.TextInput(

                attrs={

                    "placeholder":"Example: Week 1"

                }

            ),

            "prepared_by": forms.TextInput(

                attrs={

                    "placeholder":"Prepared by"

                }

            ),

        }    


# =====================================================
# DCF REPORT - STEP 2
# =====================================================

class DCFStep2Form(forms.ModelForm):

    class Meta:

        model = DCFReport

        fields = [

            "has_bswmc",

            "bswmc_members",

            "bswmc_meetings",

            "has_eo",

            "has_bswm_plan",

        ]


# =====================================================
# DCF REPORT - STEP 3
# =====================================================

class DCFStep3Form(forms.ModelForm):

    class Meta:

        model = DCFReport

        fields = [

            "has_swm_program",

            "swm_program_description",

        ]

        widgets = {

            "swm_program_description": forms.Textarea(

                attrs={

                    "rows":5,

                    "placeholder":"Describe the barangay SWM program..."

                }

            )

        }


# =====================================================
# DCF REPORT - STEP 4
# =====================================================

class DCFStep4Form(forms.ModelForm):

    class Meta:

        model = DCFReport

        fields = [

            "cleanup_drives",

            "cleanup_participants",

            "cleanup_area",

        ]

        widgets = {

            "cleanup_area": forms.TextInput(

                attrs={

                    "placeholder":"Example: Creek, Road, Coastal Area"

                }

            ),

        }


        
                