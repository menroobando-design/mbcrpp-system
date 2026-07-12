import os

import win32com.client


def convert_to_pdf(docx_file):

    pdf_file = docx_file.replace(".docx", ".pdf")

    word = win32com.client.Dispatch("Word.Application")

    word.Visible = False

    doc = word.Documents.Open(os.path.abspath(docx_file))

    # 17 = PDF format
    doc.SaveAs(
        os.path.abspath(pdf_file),
        FileFormat=17
    )

    doc.Close()

    word.Quit()

    return pdf_file