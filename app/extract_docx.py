from pathlib import Path

import docx
from docx.table import Table
from docx.text.paragraph import Paragraph

from clean import normalize, match_key


def make_entry(page_no, original_text, method):
    return {
        "page_no": page_no,
        "original_text": original_text,
        "text": normalize(original_text),
        "key": match_key(original_text),
        "method": method,
    }


def table_to_text(table):
    lines = []
    for row in table.rows:
        cells = [cell.text.strip() for cell in row.cells]
        lines.append(" | ".join(cells))
    return "\n".join(lines)


def extract_docx(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if path.suffix.lower() != ".docx":
        raise ValueError(f"Not a .docx file: {path.name}")

    doc = docx.Document(path)
    parts = []

    for child in doc.element.body.iterchildren():
        if child.tag.endswith("}p"):
            text = Paragraph(child, doc).text
            if text.strip():
                parts.append(text)
        elif child.tag.endswith("}tbl"):
            parts.append(table_to_text(Table(child, doc)))

    return [make_entry(1, "\n".join(parts), "docx")]


if __name__ == "__main__":
    files = [
        "data/demo_academy/courses.docx",
        "data/demo_academy/institute_info.docx",
    ]
    for file in files:
        print("=====", file)
        for p in extract_docx(file):
            lines = p["original_text"].split("\n")
            print(p["page_no"], p["method"], "| lines:", len(lines))
            print("  first :", repr(lines[0][:60]))
            print("  last  :", repr(lines[-1][:60]))
