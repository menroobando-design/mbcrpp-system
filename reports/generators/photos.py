import os

from PIL import Image

from reportlab.lib.units import cm


# ==================================================
# SETTINGS
# ==================================================

PHOTO_BOX_WIDTH = 8 * cm
PHOTO_BOX_HEIGHT = 10 * cm

LEFT_MARGIN = 2 * cm
TOP_MARGIN = 4 * cm
COLUMN_GAP = 1 * cm
ROW_GAP = 2 * cm


def draw_photo_pages(c, report):

    categories = [

        "Before",
        "During",
        "After",
        "Collected Waste",
        "Group Photo",
        "Attendance",

    ]

    for category in categories:

        photos = report.photos.filter(category=category)

        if not photos.exists():
            continue

        c.showPage()

        width, height = c._pagesize

        c.setFont("Helvetica-Bold", 18)

        c.drawCentredString(
            width / 2,
            height - 2 * cm,
            category.upper()
        )

        x = LEFT_MARGIN
        y = height - TOP_MARGIN

        column = 0

        for photo in photos:

            if os.path.exists(photo.image.path):

                img = Image.open(photo.image.path)

                img_w, img_h = img.size

                scale = min(
                    PHOTO_BOX_WIDTH / img_w,
                    PHOTO_BOX_HEIGHT / img_h
                )

                draw_w = img_w * scale
                draw_h = img_h * scale

                draw_x = x + (PHOTO_BOX_WIDTH - draw_w) / 2
                draw_y = y - draw_h

                c.drawImage(
                    photo.image.path,
                    draw_x,
                    draw_y,
                    width=draw_w,
                    height=draw_h,
                    preserveAspectRatio=True,
                    mask="auto",
                )

            c.setFont("Helvetica", 9)

            c.drawCentredString(
                x + PHOTO_BOX_WIDTH / 2,
                y - PHOTO_BOX_HEIGHT - .4 * cm,
                photo.caption or ""
            )

            if column == 0:

                x += PHOTO_BOX_WIDTH + COLUMN_GAP
                column = 1

            else:

                x = LEFT_MARGIN
                column = 0

                y -= PHOTO_BOX_HEIGHT + ROW_GAP

                if y < 7 * cm:

                    c.showPage()

                    c.setFont("Helvetica-Bold", 18)

                    c.drawCentredString(
                        width / 2,
                        height - 2 * cm,
                        category.upper()
                    )

                    x = LEFT_MARGIN
                    y = height - TOP_MARGIN