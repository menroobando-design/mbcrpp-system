from openpyxl import load_workbook
from django.conf import settings
import os


def generate_municipal_excel():

    template = os.path.join(
        settings.BASE_DIR,
        "report_templates",
        "kalinisan_weekly_template.xlsx",
    )

    workbook = load_workbook(template)

    sheet = workbook.active

    return workbook, sheet