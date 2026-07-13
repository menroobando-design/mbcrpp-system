import os
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_report_pdf(report):

    print("===== NEW PDF GENERATOR IS RUNNING =====")

    filename = os.path.join(
        settings.MEDIA_ROOT,
        f"Report_{report.id}.pdf"
    )

    c = canvas.Canvas(filename, pagesize=A4)

    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 800, "THIS IS THE NEW PDF GENERATOR")

    c.save()

    return filename