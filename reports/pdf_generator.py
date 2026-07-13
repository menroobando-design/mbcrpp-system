import os
from io import BytesIO

from django.conf import settings

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_report_pdf(report):

    filename = os.path.join(
        settings.MEDIA_ROOT,
        f"Report_{report.id}.pdf"
    )

    c = canvas.Canvas(
        filename,
        pagesize=A4
    )

    width, height = A4

    c.setTitle(f"Report {report.id}")

    c.drawString(
        50,
        height - 50,
        "MBCRPP REPORT"
    )

    c.save()

    return filename