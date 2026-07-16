from reportlab.lib.units import cm


def draw_signatures(c, report):

    y = 10.3 * cm

    # ------------------------------------
    # SECTION B & C
    # ------------------------------------

    c.setFont("Helvetica-Bold", 9)

    c.drawString(
        2 * cm,
        y + 1.8 * cm,
        "B. Photo Documentation (attach photos of the clean-up drive here)"
    )

    c.drawString(
        2 * cm,
        y + 1.2 * cm,
        "C. List of Attendees and Total Number of Volunteers."
    )

    # ====================================
    # PREPARED BY
    # ====================================

    c.setFont("Helvetica-Bold", 11)

    c.drawString(
        2 * cm,
        y,
        "Prepared by:"
    )

    # Name

    c.setFont("Helvetica-Bold", 10)

    c.drawCentredString(
        5.25 * cm,
        y - 1.2 * cm,
        report.barangay.committee_chair or ""
    )

    # Signature line

    c.line(
        2.5 * cm,
        y - 1.45 * cm,
        8 * cm,
        y - 1.45 * cm
    )

    # Position

    c.setFont("Helvetica", 9)

    c.drawCentredString(
        5.25 * cm,
        y - 2.0 * cm,
        "Committee Chair on Environment"
    )

    c.drawCentredString(
        5.25 * cm,
        y - 2.5 * cm,
        "or Authorized Representative"
    )

    # Date

    c.drawCentredString(
        15.75 * cm,
        y - 1.2 * cm,
        report.activity_date.strftime("%B %d, %Y")
    )

    c.line(
        13.5 * cm,
        y - 1.45 * cm,
        18 * cm,
        y - 1.45 * cm
    )

    c.drawCentredString(
        15.75 * cm,
        y - 2.0 * cm,
        "Date"
    )

    # ====================================
    # CERTIFIED CORRECT
    # ====================================

    y -= 4.3 * cm

    c.setFont("Helvetica-Bold", 11)

    c.drawString(
        2 * cm,
        y,
        "Certified Correct:"
    )

    # Name

    c.setFont("Helvetica-Bold", 10)

    c.drawCentredString(
        5.25 * cm,
        y - 1.2 * cm,
        report.barangay.barangay_captain or ""
    )

    # Signature line

    c.line(
        2.5 * cm,
        y - 1.45 * cm,
        8 * cm,
        y - 1.45 * cm
    )

    # Position

    c.setFont("Helvetica", 9)

    c.drawCentredString(
        5.25 * cm,
        y - 2.0 * cm,
        "Punong Barangay"
    )

    c.drawCentredString(
        5.25 * cm,
        y - 2.5 * cm,
        "or Authorized Representative"
    )

    # Date

    c.drawCentredString(
        15.75 * cm,
        y - 1.2 * cm,
        report.activity_date.strftime("%B %d, %Y")
    )

    c.line(
        13.5 * cm,
        y - 1.45 * cm,
        18 * cm,
        y - 1.45 * cm
    )

    c.drawCentredString(
        15.75 * cm,
        y - 2.0 * cm,
        "Date"
    )