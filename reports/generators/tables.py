from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def draw_information_table(c, report):

    width, height = c._pagesize

    y = height - 6.8 * cm

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
    # Styles
    # -------------------------------------------------

    styles = getSampleStyleSheet()

    cell_style = styles["BodyText"]
    cell_style.fontName = "Helvetica"
    cell_style.fontSize = 8
    cell_style.leading = 10

    # -------------------------------------------------
    # MAIN TABLE
    # -------------------------------------------------

    data = [

        [
            "Date",
            "Barangay",
            "Water Body/\nWaterway Covered",
            "Length\nCovered",
            "Participants",
        ],

        [
            Paragraph(
                report.activity_date.strftime("%B %d, %Y"),
                cell_style,
            ),

            Paragraph(
                report.barangay.name,
                cell_style,
            ),

            Paragraph(
                report.activity_location or "",
                cell_style,
            ),

            Paragraph(
                f"{report.length_covered} meters",
                cell_style,
            ),

            Paragraph(
                f"""
    Barangay Officials : {report.barangay_officials}<br/>
    SK Members : {report.sk_members}<br/>
    CSO Members : {report.cso_members}<br/>
    Total : {report.participants}
                """,
                cell_style,
            ),
        ]

    ]

    table = Table(

        data,

        colWidths=[
            3.2 * cm,
            2.8 * cm,
            5.8 * cm,
            2.3 * cm,
            4.0 * cm,
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

            ("TOPPADDING", (0, 0), (-1, 0), 8),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ("TOPPADDING", (0, 1), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 6),

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
            "Other Remarks",
        ],

        [
            Paragraph(
                report.disposal_method or "",
                cell_style,
            ),

            Paragraph(
                report.remarks or "",
                cell_style,
            ),
        ]

    ]

    remarks_table = Table(

        remarks,

        colWidths=[
            9 * cm,
            9 * cm,
        ]

    )

    remarks_table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

            ("BOX", (0, 0), (-1, -1), 1, colors.black),

            ("ALIGN", (0, 0), (-1, 0), "CENTER"),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("TOPPADDING", (0, 0), (-1, 0), 5),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 5),

            ("TOPPADDING", (0, 1), (-1, -1), 6),

            ("BOTTOMPADDING", (0, 1), (-1, -1), 6),

        ])

    )

    remarks_table.wrapOn(c, width, height)

    remarks_table.drawOn(
        c,
        1.3 * cm,
        y - 8.2 * cm
    )