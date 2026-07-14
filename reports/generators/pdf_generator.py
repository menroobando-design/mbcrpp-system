import os
import tempfile

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .header import draw_header
from .tables import draw_information_table
from .signatures import draw_signatures


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
    
    c.showPage()

    c.save()

    return filename