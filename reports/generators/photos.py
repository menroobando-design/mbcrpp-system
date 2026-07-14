import os

from reportlab.lib.units import cm


PHOTO_SIZE = 7 * cm


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

        x = 2 * cm
        y = height - 4 * cm

        count = 0

        for photo in photos:

            if os.path.exists(photo.image.path):

                c.drawImage(

                    photo.image.path,

                    x,

                    y - PHOTO_SIZE,

                    width=PHOTO_SIZE,

                    height=PHOTO_SIZE,

                    preserveAspectRatio=True,

                    mask="auto",

                )

            c.setFont("Helvetica", 10)

            c.drawCentredString(

                x + PHOTO_SIZE / 2,

                y - PHOTO_SIZE - .4 * cm,

                photo.caption or ""

            )

            count += 1

            if count % 2 == 1:

                x = 11 * cm

            else:

                x = 2 * cm

                y -= 9 * cm

                if y < 6 * cm:

                    c.showPage()

                    y = height - 4 * cm