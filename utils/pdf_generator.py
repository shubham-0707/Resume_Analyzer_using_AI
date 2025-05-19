from fpdf import FPDF
from io import BytesIO

def generate_pdf_report(score, fit, suggestions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Resume Analysis Report", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(180, 10, f"AI Job Match: {fit[0]} ({fit[1]*100:.1f}%)")
    pdf.multi_cell(180, 10, f"ATS Score: {score}/100")
    pdf.ln(5)

    pdf.cell(0, 10, "Suggestions:", ln=True)
    for tip in suggestions:
        pdf.multi_cell(180, 10, f"- {tip}")

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer