from reportlab.lib.units import cm


def draw_signatures(c, report):

    width, height = c._pagesize

    y = 8.2 * cm

    # ---------------------------------
    # SECTION B & C
    # ---------------------------------

    c.setFont("Helvetica-Bold", 10)

    c.drawString(
        2 * cm,
        y + 1 * cm,
        "B. Photo Documentation (attach photos of the clean-up drive here)"
    )

    c.drawString(
        2 * cm,
        y + 0.8 * cm,
        "C. List of Attendees and Total Number of Volunteers."
    )

    # -----------------------------
    # Prepared by
    # -----------------------------

    c.setFont("Helvetica-Bold", 11)
    c.drawString(2 * cm, y, "Prepared by:")

    # Signature line
    c.line(2.5 * cm, y - 1.4 * cm, 8 * cm, y - 1.4 * cm)

    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(
        5.25 * cm,
        y - 1.8 * cm,
        report.barangay.committee_chair or ""
    )

    c.setFont("Helvetica", 9)

    c.drawCentredString(
        5.25 * cm,
        y - 2.4 * cm,
        "Committee Chair on Environment"
    )

    c.drawCentredString(
        5.25 * cm,
        y - 2.9 * cm,
        "or Authorized Representative"
    )

    # Date

    c.line(13.5 * cm, y - 1.4 * cm, 18 * cm, y - 1.4 * cm)

    c.drawCentredString(
        15.75 * cm,
        y - 1.8 * cm,
        report.activity_date.strftime("%B %d, %Y")
    )

    c.drawCentredString(
        15.75 * cm,
        y - 2.4 * cm,
        "Date"
    )

    # -----------------------------
    # Certified Correct
    # -----------------------------

    y -= 4.3 * cm

    c.setFont("Helvetica-Bold", 11)

    c.drawString(
        2 * cm,
        y,
        "Certified Correct:"
    )

    c.line(
        2.5 * cm,
        y - 1.4 * cm,
        8 * cm,
        y - 1.4 * cm
    )

    c.setFont("Helvetica-Bold", 10)

    c.drawCentredString(
        5.25 * cm,
        y - 1.8 * cm,
        report.barangay.barangay_captain or ""
    )

    c.setFont("Helvetica", 9)

    c.drawCentredString(
        5.25 * cm,
        y - 2.4 * cm,
        "Punong Barangay"
    )

    c.drawCentredString(
        5.25 * cm,
        y - 2.9 * cm,
        "or Authorized Representative"
    )

    c.line(
        13.5 * cm,
        y - 1.4 * cm,
        18 * cm,
        y - 1.4 * cm
    )

    c.drawCentredString(
        15.75 * cm,
        y - 1.8 * cm,
        report.activity_date.strftime("%B %d, %Y")
    )

    c.drawCentredString(
        15.75 * cm,
        y - 2.4 * cm,
        "Date"
    )