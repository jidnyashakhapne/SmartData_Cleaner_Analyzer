from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def make_pdf_report(filename, original, cleaned, log, profile):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    story = [Paragraph("SmartData Cleaner &amp; Analyzer - Data Quality Summary", styles["Title"]),
             Spacer(1, 12), Paragraph(f"File: {filename}", styles["Normal"]),
             Paragraph(f"Original shape: {original.shape[0]} rows x {original.shape[1]} columns", styles["Normal"]),
             Paragraph(f"Cleaned shape: {cleaned.shape[0]} rows x {cleaned.shape[1]} columns", styles["Normal"]),
             Paragraph(f"Missing cells in original: {int(original.isna().sum().sum())}", styles["Normal"]),
             Paragraph(f"Exact duplicate rows in original: {int(original.duplicated().sum())}", styles["Normal"]),
             Spacer(1, 12), Paragraph("Cleaning log", styles["Heading2"])]
    data = [["Operation", "Affected rows", "Details"]]
    for item in log:
        data.append([str(item["operation"]), str(item["affected_rows"]), str(item["details"])[:100]])
    table = Table(data, repeatRows=1, colWidths=[150, 75, 270])
    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#243B53")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),0.4,colors.grey),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("FONTSIZE",(0,0),(-1,-1),8),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#F2F5F8")])
    ]))
    story.append(table)
    story.append(Spacer(1, 12))
    story.append(Paragraph("Column profile", styles["Heading2"]))
    pdata = [["Column", "Type", "Missing", "Unique"]]
    for _, r in profile.iterrows():
        pdata.append([str(r["column"])[:28], str(r["inferred_type"]),
                      str(r["missing_count"]), str(r["unique_count"])])
    ptable = Table(pdata, repeatRows=1, colWidths=[180, 120, 70, 70])
    ptable.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#243B53")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),0.4,colors.grey),
        ("FONTSIZE",(0,0),(-1,-1),8),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, colors.HexColor("#F2F5F8")])
    ]))
    story.append(ptable)
    doc.build(story)
    return buf.getvalue()
