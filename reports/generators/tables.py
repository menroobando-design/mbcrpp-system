from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle


def draw_information_table(c, report):

    width, height = c._pagesize

    y = height - 9 * cm

    # -------------------------------------------------
    # BARANGAY
    # -------------------------------------------------

    c.setFont("Helvetica-Bold", 10)

    c.drawString(
        2 * cm,
        y,
        f"BARANGAY: {report.barangay.name.upper()}"
    )

    c.drawString(
        2 * cm,
        y - .7 * cm,
        "CITY: OBANDO"
    )

    c.drawString(
        2.6 * cm,
        y - 1.5 * cm,
        "A. Barangay Clean-up Drive"
    )

    # -------------------------------------------------
    # MAIN TABLE
    # -------------------------------------------------

    data = [

        [
            "Date",
            "Barangay",
            "Water Body/\nWaterway Covered",
            "Length\nCovered",
            "Volume of Waste\nCollected"
        ],

        [
            report.activity_date.strftime("%B %d, %Y"),
            report.barangay.name,
            report.activity_location,
            "17 meters",
            f"{report.total_waste} kilograms"
        ]

    ]

    table = Table(

        data,

        colWidths=[
            4 * cm,
            3 * cm,
            3.8 * cm,
            2.8 * cm,
            3.6 * cm
        ]

    )

    table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

            ("BOX", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 0), (-1, 0), colors.white),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ("TOPPADDING", (0, 0), (-1, 0), 8),

        ])

    )

    table.wrapOn(c, width, height)

    table.drawOn(
        c,
        1.3 * cm,
        y - 5.2 * cm
    )

    # -------------------------------------------------
    # REMARKS TABLE
    # -------------------------------------------------

    remarks = [

        [
            "Details on Disposal",
            "Other Remarks"
        ],

        [
            report.disposal_method,
            report.remarks
        ]

    ]

    remarks_table = Table(

        remarks,

        colWidths=[9 * cm, 9 * cm]

    )

    remarks_table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

            ("BOX", (0, 0), (-1, -1), 1, colors.black),

            ("ALIGN", (0, 0), (-1, 0), "CENTER"),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 5),

            ("TOPPADDING", (0, 0), (-1, 0), 5),

        ])

    )

    remarks_table.wrapOn(c, width, height)

    remarks_table.drawOn(
        c,
        1.3 * cm,
        y - 8.2 * cm
    )