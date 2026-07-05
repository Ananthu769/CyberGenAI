from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

import os


def generate_pdf(filename, report):

    os.makedirs("reports", exist_ok=True)

    pdf_path = f"reports/{filename}.pdf"

    styles = getSampleStyleSheet()

    document = SimpleDocTemplate(pdf_path)

    elements = []

    elements.append(
        Paragraph(
            "<b>CyberGen AI Incident Report</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(report.replace("\n","<br/>"),
        styles["BodyText"])
    )

    document.build(elements)

    return pdf_path