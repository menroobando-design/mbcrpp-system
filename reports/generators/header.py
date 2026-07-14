import os

from django.conf import settings

from reportlab.lib.units import cm
from reportlab.lib.colors import black


def draw_header(c, report):

    width, height = c._pagesize

    # ---------------------------------------------------
    # LOGO PATHS
    # ---------------------------------------------------

    obando_logo = os.path.join(
        settings.BASE_DIR,
        "static",
        "images",
        "obando.png"
    )

    bagong_logo = os.path.join(
        settings.BASE_DIR,
        "static",
        "images",
        "bagong.png"
    )

    # Barangay logo

    barangay_logo = None

    if report.barangay.logo:

        barangay_logo = report.barangay.logo.path

    # ---------------------------------------------------
    # DRAW LOGOS
    # ---------------------------------------------------

    logo_size = 2.5 * cm

    if os.path.exists(obando_logo):

        c.drawImage(
            obando_logo,
            2 * cm,
            height - 4 * cm,
            width=logo_size,
            height=logo_size,
            preserveAspectRatio=True,
            mask="auto",
        )

    if barangay_logo and os.path.exists(barangay_logo):

        c.drawImage(
            barangay_logo,
            8.8 * cm,
            height - 4 * cm,
            width=logo_size,
            height=logo_size,
            preserveAspectRatio=True,
            mask="auto",
        )

    if os.path.exists(bagong_logo):

        c.drawImage(
            bagong_logo,
            width - 4.5 * cm,
            height - 4 * cm,
            width=logo_size,
            height=logo_size,
            preserveAspectRatio=True,
            mask="auto",
        )

    # ---------------------------------------------------
    # HEADER TEXT
    # ---------------------------------------------------

    c.setFillColor(black)

    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 1.2 * cm, "Republic of the Philippines")

    c.drawCentredString(width / 2, height - 1.7 * cm, "Province of Bulacan")

    c.drawCentredString(width / 2, height - 2.2 * cm, "Municipality of Obando")

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(
        width / 2,
        height - 2.9 * cm,
        f"BARANGAY {report.barangay.name.upper()}"
    )

    # Annex

    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(
        width - 2 * cm,
        height - 1.2 * cm,
        'ANNEX "A"'
    )

    # Form

    c.setFont("Helvetica", 9)

    c.drawCentredString(
        width / 2,
        height - 4.4 * cm,
        "(Form 1 Barangay)"
    )

    c.setFont("Helvetica-Bold", 11)

    c.drawCentredString(
        width / 2,
        height - 5.0 * cm,
        "MANILA BAY CLEAN-UP, REHABILITATION AND PRESERVATION PROGRAM"
    )

    c.setFont("Helvetica", 10)

    c.drawString(
        2 * cm,
        height - 6.0 * cm,
        f"Date : {report.activity_date.strftime('%B %d, %Y')}"
    )

    c.setFont("Helvetica-Bold", 11)

    c.drawCentredString(
        width / 2,
        height - 6.0 * cm,
        "CONDUCT OF WEEKLY CLEAN-UP DRIVE"
    )