from __future__ import annotations

from pathlib import Path
import re

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm

from src.report import generate_monthly_report

REPORT_DIR = Path("reports/generated")


def clean_markdown_line(line: str) -> str:
    line = re.sub(r"^#+\s*", "", line)
    line = line.replace("**", "")
    line = line.replace("`", "")
    line = line.replace("|", " | ")
    return line.strip()


def markdown_to_pdf(md_path: str | Path, pdf_path: str | Path | None = None) -> Path:
    md_path = Path(md_path)
    if pdf_path is None:
        pdf_path = md_path.with_suffix(".pdf")
    pdf_path = Path(pdf_path)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    story = []
    for raw_line in md_path.read_text(encoding="utf-8").splitlines():
        line = clean_markdown_line(raw_line)
        if not line:
            story.append(Spacer(1, 0.25 * cm))
            continue
        if raw_line.startswith("# "):
            story.append(Paragraph(line, styles["Title"]))
        elif raw_line.startswith("## "):
            story.append(Paragraph(line, styles["Heading2"]))
        elif raw_line.startswith("- ") or raw_line.startswith("1. "):
            story.append(Paragraph(line, styles["Bullet"]))
        else:
            story.append(Paragraph(line, styles["BodyText"]))
        story.append(Spacer(1, 0.12 * cm))

    doc.build(story)
    return pdf_path


def export_latest_report_to_pdf() -> Path:
    reports = sorted(REPORT_DIR.glob("radar_report_*.md"))
    if not reports:
        md_path = generate_monthly_report()
    else:
        md_path = reports[-1]
    return markdown_to_pdf(md_path)


if __name__ == "__main__":
    print(export_latest_report_to_pdf())
