from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from xml.sax.saxutils import escape
import os


def generate_pdf(filename, report):

    os.makedirs("reports", exist_ok=True)

    pdf_path = f"reports/{filename}.pdf"

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(pdf_path)

    story = []

    story.append(
        Paragraph(
            "<b>CyberGen AI Incident Report</b>",
            styles["Title"]
        )
    )

    # Escape all special HTML characters
    safe_report = escape(str(report))

    safe_report = safe_report.replace("\n", "<br/>")

    story.append(
        Paragraph(
            safe_report,
            styles["BodyText"]
        )
    )

    doc.build(story)

    return pdf_path