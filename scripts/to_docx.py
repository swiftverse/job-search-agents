#!/usr/bin/env python3
"""Turns a tailored resume.md into a plain Word file. Usage: to_docx.py path/to/resume.md"""
import re
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, Inches
except ImportError:
    sys.exit("Needs python-docx. Install it with: pip install python-docx")


def clean(text: str) -> str:
    return re.sub(r"\*\*|`", "", text).strip()


def spaced(paragraph, before=0, after=2):
    paragraph.paragraph_format.space_before = Pt(before)
    paragraph.paragraph_format.space_after = Pt(after)
    return paragraph


def convert(source: Path) -> Path:
    doc = Document()
    section = doc.sections[0]
    section.left_margin = section.right_margin = Inches(0.8)
    section.top_margin = section.bottom_margin = Inches(0.7)
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)

    lines = source.read_text().splitlines()
    after_name = False
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# "):
            para = spaced(doc.add_paragraph(), after=0)
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(clean(line[2:]))
            run.bold = True
            run.font.size = Pt(18)
            after_name = True
        elif after_name and not line.startswith("#"):
            para = spaced(doc.add_paragraph(clean(line)), after=8)
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            after_name = False
        elif line.startswith("## "):
            run = spaced(doc.add_paragraph(), before=10, after=3).add_run(clean(line[3:]).upper())
            run.bold = True
            run.font.size = Pt(11)
        elif line.startswith("### "):
            run = spaced(doc.add_paragraph(), before=6).add_run(clean(line[4:]))
            run.bold = True
        elif line.startswith("- "):
            spaced(doc.add_paragraph(clean(line[2:]), style="List Bullet"))
        else:
            spaced(doc.add_paragraph(clean(line)), after=4)

    target = source.with_suffix(".docx")
    doc.save(target)
    return target


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(convert(Path(sys.argv[1])))
