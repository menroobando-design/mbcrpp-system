import os
import tempfile

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .header import draw_header
from .tables import draw_information_table
from .signatures import draw_signatures
from .photos import draw_photo_pages
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch


def draw_photo_page(c, title, photos):
    """
    Draws one category page.
    Maximum of 2 photos per page.
    """

    width, height = A4

    index = 0

    while index < len(photos):

        c.showPage()

        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(width / 2, height - 45, title.upper())

        y = height - 180

        for _ in range(2):

            if index >= len(photos):
                break

            photo = photos[index]

            try:
                img = ImageReader(photo.image.path)

                c.drawImage(
                    img,
                    120,
                    y,
                    width=4.3 * inch,
                    height=3.2 * inch,
                    preserveAspectRatio=True,
                    anchor="c",
                )

            except Exception:
                c.drawString(120, y, "Unable to load image.")

            y -= 270
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
    
    c.showPage()

    c.save()

    return filename