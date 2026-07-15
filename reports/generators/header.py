import os

from django.conf import settings
from reportlab.lib.units import cm
from reportlab.lib.colors import black


def draw_header(c, report):

    width, height = c._pagesize

    # ---------------------------------------------------
    # LOGO PATHS
    # ---------------------------------------------------

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

    from reportlab.lib.utils import ImageReader

    if barangay_logo and os.path.exists(barangay_logo):

        try:
            img = ImageReader(barangay_logo)

            c.drawImage(
                img,
                2 * cm,
                height - 4 * cm,
                width=logo_size,
                height=logo_size,
                preserveAspectRatio=True,
                mask="auto",
            )

        except Exception as e:
            print("ERROR DRAWING LOGO:", e)

            c.setFillColorRGB(1, 0, 0)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(
                2 * cm,
                height - 5 * cm,
                "BARANGAY LOGO FAILED"
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
    c.drawCentredString(
        width / 2,
        height - 1.2 * cm,
        "Republic of the Philippines"
    )

    c.drawCentredString(
        width / 2,
        height - 1.7 * cm,
        "Province of Bulacan"
    )

    c.drawCentredString(
        width / 2,
        height - 2.2 * cm,
        "Municipality of Obando"
    )

    c.setFont("Helvetica-Bold", 12)

    c.drawCentredString(
        width / 2,
        height - 2.9 * cm,
        f"BARANGAY {report.barangay.name.upper()}"
    )

    # ---------------------------------------------------
    # ANNEX
    # ---------------------------------------------------

    c.setFont("Helvetica-Bold", 10)

    c.drawCentredString(
        width - 3.25 * cm,
        height - 4.4 * cm,
        'ANNEX "A"'
    )

    # ---------------------------------------------------
    # FORM
    # ---------------------------------------------------

    c.setFont("Helvetica-Oblique", 8)

    c.drawCentredString(
        3.5 * cm,
        height - 4.4 * cm,
        "(Form 1 Barangay)"
    )

    # ---------------------------------------------------
    # TITLE
    # ---------------------------------------------------

    c.setFont("Helvetica-Bold", 11)

    c.drawCentredString(
        width / 2,
        height - 5.0 * cm,
        "MANILA BAY CLEAN-UP, REHABILITATION AND PRESERVATION PROGRAM"
    )

    # ---------------------------------------------------
    # DATE
    # ---------------------------------------------------

    c.setFont("Helvetica", 10)

    c.drawString(
        9 * cm,
        height - 5.7 * cm,
        f"Date : {report.activity_date.strftime('%B %d, %Y')}"
    )

    # ---------------------------------------------------
    # ACTIVITY TITLE
    # ---------------------------------------------------

    c.setFont("Helvetica-Bold", 11)

    c.drawCentredString(
        width / 2,
        height - 6.4 * cm,
        "CONDUCT OF WEEKLY CLEAN-UP DRIVE"
    )