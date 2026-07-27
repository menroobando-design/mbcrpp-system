import os
import tempfile

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .header import draw_header
from .tables import draw_information_table
from .signatures import draw_signatures
from reportlab.lib.utils import ImageReader
from urllib.request import urlopen
from reportlab.lib.units import inch, cm

# ====================================
# PHOTO SETTINGS
# ====================================

PHOTO_WIDTH = 15 * cm
PHOTO_HEIGHT = 8 * cm


def draw_photo_page(c, title, photos):

    width, height = A4

    index = 0

    while index < len(photos):

        c.showPage()

        # ---------------------------------
        # Page Title
        # ---------------------------------

        c.setFont("Helvetica-Bold", 16)

        c.drawCentredString(
            width / 2,
            height - 1.5 * cm,
            title.upper()
        )

        # Two photo slots per page

        positions = [

            height - 9 * cm,
            height - 19 * cm,

        ]

        for y in positions:

            if index >= len(photos):
                break

            photo = photos[index]

            try:

                img = ImageReader(urlopen(photo.image.url))

                img_width, img_height = img.getSize()

                # Maximum box size

                max_width = 15 * cm
                max_height = 8 * cm

                scale = min(
                    max_width / img_width,
                    max_height / img_height
                )

                draw_width = img_width * scale
                draw_height = img_height * scale

                x = (width - draw_width) / 2

                # -----------------------------
                # Border
                # -----------------------------

                c.setStrokeColorRGB(0.75, 0.75, 0.75)

                c.rect(
                    x - 4,
                    y - 4,
                    draw_width + 8,
                    draw_height + 8
                )

                # -----------------------------
                # Draw Image
                # -----------------------------

                c.drawImage(

                    img,

                    x,

                    y,

                    width=draw_width,

                    height=draw_height,

                    preserveAspectRatio=True,

                    mask="auto",

                )

                # -----------------------------
                # Caption
                # -----------------------------

                c.setFont("Helvetica", 10)

                c.drawCentredString(

                    width / 2,

                    y - .6 * cm,

                    photo.caption if photo.caption else ""

                )

            except Exception as e:

                print("IMAGE ERROR:", e)

                c.drawCentredString(

                    width / 2,

                    y,

                    "Unable to load image."

                )

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