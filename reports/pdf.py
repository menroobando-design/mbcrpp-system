from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

def generate_report_pdf(report):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=(8.27 * inch, 11.69 * inch),   # A4 Portrait
        rightMargin=35,
        leftMargin=35,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    normal = styles["BodyText"]
    normal.alignment = TA_CENTER

    elements = []

    # Barangay Logo
    if report.barangay.logo:

        logo = Image(
            report.barangay.logo.path,
            width=0.9 * inch,
            height=0.9 * inch
        )

        logo.hAlign = "CENTER"

        elements.append(logo)

    elements.append(
        Paragraph("<b>Republic of the Philippines</b>", normal)
    )

    elements.append(
        Paragraph("Province of Bulacan", normal)
    )

    elements.append(
        Paragraph("Municipality of Obando", normal)
    )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            f"<b>{report.barangay.name.upper()}</b>",
            title
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    # ===========================
    # REPORT INFORMATION
    # ===========================

    data = [

        ["Date", str(report.activity_date)],

        ["Barangay", report.barangay.name],

        ["Week Covered", report.week_covered],

        ["Location", report.activity_location],

        ["Participants", str(report.participants)],

        ["Biodegradable", f"{report.biodegradable} kg"],

        ["Recyclable", f"{report.recyclable} kg"],

        ["Residual", f"{report.residual} kg"],

        ["Potential", f"{report.potential} kg"],

        ["TOTAL", f"{report.total_waste} kg"],

        ["Method of Disposal", report.disposal_method],

    ]

    table = Table(
        data,
        colWidths=[170, 240]
    )

    table.setStyle(

        TableStyle([

            ("GRID", (0,0), (-1,-1), 1, colors.black),

            ("BACKGROUND", (0,0), (0,-1), colors.lightgrey),

            ("FONTNAME", (0,0), (-1,-1), "Helvetica"),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8),

            ("VALIGN", (0,0), (-1,-1), "TOP"),

        ])

    )

    elements.append(table)

    elements.append(
        Spacer(1,20)
    )

    elements.append(
        Paragraph(
            "<b>Remarks</b>",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            report.remarks if report.remarks else "-",
            styles["BodyText"]
        )
    )

    doc.build(elements)

    buffer.seek(0)

    return buffer