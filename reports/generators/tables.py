from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors


def draw_information_table(c, report):

    width, height = c._pagesize

    data = [

        ["BARANGAY", report.barangay.name],

        ["CITY / MUNICIPALITY", "OBANDO"],

        ["SECTION", "A. Barangay Clean-up Drive"],

    ]

    table = Table(
        data,
        colWidths=[5 * cm, 11 * cm]
    )

    table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),

            ("FONTSIZE", (0, 0), (-1, -1), 10),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),

        ])

    )

    table.wrapOn(c, width, height)

    table.drawOn(
        c,
        2 * cm,
        height - 9.2 * cm
    )