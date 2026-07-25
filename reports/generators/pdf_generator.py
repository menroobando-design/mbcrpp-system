import os
import tempfile

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .header import draw_header
from .tables import draw_information_table
from .signatures import draw_signatures
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch, cm

# ====================================
# PHOTO SETTINGS
# ====================================

PHOTO_WIDTH = 10 * cm
PHOTO_HEIGHT = 16 * cm


def draw_photo_page(c, title, photos):
    """
    Draw one category page.
    Maximum of 2 photos per page.
    Images fit inside a 10cm × 16cm box while preserving aspect ratio.
    """

    width, height = A4

    index = 0

    while index < len(photos):

        c.showPage()

        # -------------------------
        # Title
        # -------------------------

        c.setFont("Helvetica-Bold", 13)

        c.drawCentredString(
            width / 2,
            height - 45,
            title.upper()
        )

        # Top image position

        positions = [

            height - 250,

            height - 520,

        ]

        for y in positions:

            if index >= len(photos):
                break

            photo = photos[index]

            try:

                img = ImageReader(photo.image.path)

                # -------------------------
                # Get original image size
                # -------------------------

                img_width, img_height = img.getSize()

                scale = min(
                    PHOTO_WIDTH / img_width,
                    PHOTO_HEIGHT / img_height
                )

                draw_width = img_width * scale
                draw_height = img_height * scale

                x = (width - draw_width) / 2

                c.drawImage(

                    img,

                    x,

                    y,

                    width=draw_width,

                    height=draw_height,

                    preserveAspectRatio=True,

                )

            except Exception as e:
                print("IMAGE ERROR:", e)
                c.drawString(120, y, "Unable to load image.")

            index += 1


def generate_report_pdf(report):

    filename = os.path.join(
        tempfile.gettempdir(),
        f"Report_{report.id}.pdf"
    )

    c = canvas.Canvas(
        filename,
        pagesize=A4
    )

    # ----------------------------------
    # PAGE 1
    # ----------------------------------

    draw_header(c, report)

    draw_information_table(c, report)

    draw_signatures(c, report)

    photo_categories = [

        ("Before", report.photos.filter(category="Before")),

        ("During", report.photos.filter(category="During")),

        ("After", report.photos.filter(category="After")),

        ("Group Photo", report.photos.filter(category="Group Photo")),

        ("Collected Wastes", report.photos.filter(category="Collected Waste")),

        ("Attendance", report.photos.filter(category="Attendance")),

    ]

    for title, queryset in photo_categories:

        photos = list(queryset)

        if photos:

            draw_photo_page(c, title, photos)

    c.save()

    return filename