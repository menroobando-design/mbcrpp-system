import os
import tempfile

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_report_pdf(report):

    filename = os.path.join(
        tempfile.gettempdir(),
        f"Report_{report.id}.pdf"
    )

    c = canvas.Canvas(filename, pagesize=A4)

    c.setTitle(f"Report {report.id}")

    c.drawString(
        50,
        800,
        "MBCRPP REPORT"
    )

    c.save()

    return filename