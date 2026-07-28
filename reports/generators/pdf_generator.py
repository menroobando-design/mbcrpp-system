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

PHOTO_WIDTH = 16 * cm
PHOTO_HEIGHT = 9 * cm

TOP_MARGIN = 1 * inch
BOTTOM_MARGIN = 1 * inch
LEFT_MARGIN = 1 * inch
RIGHT_MARGIN = 1 * inch

PHOTO_GAP = 1 * cm

def draw_photo_page(c, title, photos):

    width, height = A4

    index = 0

    while index < len(photos):

        c.showPage()

        # ---------------------------------
        # Page Title
        # ---------------------------------

        c.setFont("Helvetica-Bold", 16)

        # ---------------------------------
        # 1-inch top margin
        # ---------------------------------

        TOP_MARGIN = 1 * inch

        c.drawCentredString(
            width / 2,
            height - 0.6 * inch,
            title.upper()
        )

        # Leave some space below the title

        # ---------------------------------
        # Compute printable area
        # ---------------------------------

        usable_height = height - TOP_MARGIN - BOTTOM_MARGIN

        first_photo_y = height - TOP_MARGIN - PHOTO_HEIGHT

        second_photo_y = first_photo_y - PHOTO_HEIGHT - PHOTO_GAP

        positions = [

            first_photo_y,

            second_photo_y,

        ]

        for y in positions:

            if index >= len(photos):
                break

            photo = photos[index]

            try:

                img = ImageReader(urlopen(photo.image.url))

                img_width, img_height = img.getSize()

                # ----------------------------------------
                # Detect image orientation automatically
                # ----------------------------------------

                if img_width >= img_height:
                    # Landscape photo
                    scale = PHOTO_WIDTH / img_width
                else:
                    # Portrait photo
                    scale = PHOTO_HEIGHT / img_height

                draw_width = img_width * scale
                draw_height = img_height * scale

                # Never exceed the maximum frame
                if draw_width > PHOTO_WIDTH:
                    scale = PHOTO_WIDTH / draw_width
                    draw_width *= scale
                    draw_height *= scale

                if draw_height > PHOTO_HEIGHT:
                    scale = PHOTO_HEIGHT / draw_height
                    draw_width *= scale
                    draw_height *= scale

                # Center inside the frame
                frame_x = LEFT_MARGIN + (
                    (width - LEFT_MARGIN - RIGHT_MARGIN - PHOTO_WIDTH) / 2
                )
                frame_y = y

                x = frame_x + (PHOTO_WIDTH - draw_width) / 2
                image_y = frame_y + (PHOTO_HEIGHT - draw_height) / 2

                # Draw a light border around the frame
                c.setLineWidth(0.5)
                c.rect(frame_x, frame_y, PHOTO_WIDTH, PHOTO_HEIGHT)

                c.drawImage(
                    img,
                    x,
                    image_y,
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

                    y - 0.6 * inch,

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