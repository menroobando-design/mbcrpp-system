from django import forms
from .widgets import MultipleFileInput
from .models import (
    WeeklyReport,
    ReportPhoto,
    DCFReport,
)


# ==========================================
# Multiple File Upload Field
# ==========================================

class MultipleFileField(forms.FileField):

    widget = MultipleFileInput

    def clean(self, data, initial=None):

        if not data:
            return []

        if isinstance(data, (list, tuple)):
            return data

        return [data]


# ==========================================
# Weekly Report Form
# ==========================================

class WeeklyReportForm(forms.ModelForm):

    before_photos = MultipleFileField(required=False)

    during_photos = MultipleFileField(required=False)

    after_photos = MultipleFileField(required=False)

    waste_photos = MultipleFileField(required=False)

    group_photos = MultipleFileField(required=False)

    attendance_photos = MultipleFileField(required=False)

    class Meta:

        model = WeeklyReport

        labels = {

            "barangay_officials": "No. of Barangay Officials",

            "sk_members": "No. of Sangguniang Kabataan",

            "cso_members": "No. of Civil Society Organization (CSO)",

            "disposal_method": "Method of Disposal",

        }

        fields = [

            "week_covered",

            "activity_date",

            "activity_location",

            "length_covered",

            "volume_of_waste",

            # Waste Collected
            "biodegradable",
            "recyclable",
            "residual",

            # Participants
            "barangay_officials",

            "sk_members",

            "cso_members",

            "disposal_method",

            "remarks",

        ]   

        widgets = {

            "activity_date": forms.DateInput(
                attrs={"type": "date"}
            ),

            "activity_location": forms.TextInput(
                attrs={
                    "placeholder": "Activity Location"
                }
            ),

            "length_covered": forms.NumberInput(
                attrs={
                    "placeholder": "Length Covered (meters)"
                }
            ),

            "volume_of_waste": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "placeholder": "Total Waste Collected (kg)"
                }
            ),

            "biodegradable": forms.NumberInput(
                attrs={
                    "placeholder": "Biodegradable (kg)",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "recyclable": forms.NumberInput(
                attrs={
                    "placeholder": "Recyclable (kg)",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "residual": forms.NumberInput(
                attrs={
                    "placeholder": "Residual (kg)",
                    "step": "0.01",
                    "min": "0",
                }
            ),
        

            "barangay_officials": forms.NumberInput(
                attrs={"min": 0}
            ),

            "sk_members": forms.NumberInput(
                attrs={"min": 0}
            ),

            "cso_members": forms.NumberInput(
                attrs={"min": 0}
            ),

            "disposal_method": forms.Textarea(
                attrs={"rows": 3}
            ),

            "remarks": forms.Textarea(
                attrs={"rows": 3}
            ),

        }


# ==========================================
# Old Upload Form (temporary)
# ==========================================

class ReportPhotoForm(forms.Form):

    category = forms.ChoiceField(
        choices=ReportPhoto.CATEGORY_CHOICES
    )

    images = MultipleFileField()

    caption = forms.CharField(
        required=False
    )


# =====================================================
# DCF REPORT 
# =====================================================

class DCFReportForm(forms.ModelForm):

    class Meta:

        model = DCFReport

        fields = [

            # =========================
            # GENERAL
            # =========================

            "month",
            "year",
            "week_covered",

            # =========================
            # A. BSWMC
            # =========================

            "has_bswmc",
            "bswmc_members",
            "bswmc_meetings",
            "has_eo",
            "has_bswm_plan",

            # =========================
            # B. SWM Program
            # =========================

            "has_swm_program",
            "swm_program_description",

            # =========================
            # C. Weekly Clean-up
            # =========================

            "cleanup_drives",
            "cleanup_participants",
            "cleanup_area",

            # =========================
            # D. Segregation
            # =========================

            "segregation_implemented",
            "collection_schedule",
            "households_served",
            "households_compliant",

            # =========================
            # E. MRF
            # =========================

            "has_mrf",
            "mrf_location",
            "mrf_operational",
            "mrf_workers",

            # =========================
            # F. Waste Diversion
            # =========================

            "biodegradable",
            "recyclable",
            "residual",

            # =========================
            # G. Enforcement
            # =========================

            "has_ordinance",
            "violations_recorded",
            "penalties_imposed",

            # =========================
            # H. IEC
            # =========================

            "iec_activities",
            "iec_participants",
            "best_practices",

            # =========================
            # Certification
            # =========================

            "prepared_by",
            "certified_by",

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
                    "placeholder":"Week Covered"
                }
            ),

            "swm_program_description": forms.Textarea(
                attrs={
                    "rows":3
                }
            ),

            "best_practices": forms.Textarea(
                attrs={
                    "rows":3
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


        
                