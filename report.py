from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(result, filename="report.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("SkillBridge AI Report", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Overall Score: {result['overall_score']}", styles["Normal"]))
    content.append(Paragraph(f"Confidence: {result['confidence']}%", styles["Normal"]))
    content.append(Spacer(1, 10))

    for r in result["skills"]:
        content.append(Paragraph(f"Skill: {r['skill']}", styles["Heading3"]))
        content.append(Paragraph(f"Required: {r['required']} | Score: {r['score']} | Gap: {r['raw_gap']}", styles["Normal"]))
        content.append(Paragraph(f"Feedback: {r['feedback']}", styles["Normal"]))
        content.append(Spacer(1, 10))

    doc.build(content)
    return filename
