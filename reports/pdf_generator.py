import os
import tempfile

from django.conf import settings

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def generate_report_pdf(report):

    filename = os.path.join(
        tempfile.gettempdir(),
        f"Report_{report.id}.pdf"
    )

    c = canvas.Canvas(filename, pagesize=A4)

    width, height = A4

    # ==========================
    # LOGOS
    # ==========================

    obando_logo = os.path.join(
        settings.BASE_DIR,
        "static",
        "images",
        "obando.png"
    )

    menro_logo = os.path.join(
        settings.BASE_DIR,
        "static",
        "images",
        "menro.png"
    )

    barangay_logo = None

    if report.barangay.logo:
        barangay_logo = report.barangay.logo.path

    if os.path.exists(obando_logo):
        c.drawImage(
            obando_logo,
            2 * cm,
            height - 4 * cm,
            width=2.5 * cm,
            height=2.5 * cm,
            preserveAspectRatio=True,
        )

    if barangay_logo and os.path.exists(barangay_logo):
        c.drawImage(
            barangay_logo,
            width / 2 - 1.25 * cm,
            height - 4 * cm,
            width=2.5 * cm,
            height=2.5 * cm,
            preserveAspectRatio=True,
        )

    if os.path.exists(menro_logo):
        c.drawImage(
            menro_logo,
            width - 4.5 * cm,
            height - 4 * cm,
            width=2.5 * cm,
            height=2.5 * cm,
            preserveAspectRatio=True,
        )

    # ==========================
    # HEADER
    # ==========================

    c.setFont("Helvetica", 11)

    c.drawCentredString(
        width / 2,
        height - 1.2 * cm,
        "Republic of the Philippines"
    )

    c.drawCentredString(
        width / 2,
        height - 1.8 * cm,
        "Municipality of Obando"
    )

    c.drawCentredString(
        width / 2,
        height - 2.4 * cm,
        "Municipal Environment and Natural Resources Office"
    )

    c.setFont("Helvetica-Bold", 16)

    c.setFillColor(HexColor("#0B7A3E"))

    c.drawCentredString(
        width / 2,
        height - 5 * cm,
        "MBCRPP WEEKLY REPORT"
    )

    c.setFillColor(HexColor("#000000"))

    c.save()

    return filename