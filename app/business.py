from pathlib import Path

import docx
from docling.document_converter import DocumentConverter

from extract_docx import make_entry

# Files that hold records (read exactly, cell by cell, with python-docx).
# Every other .docx in the folder is a prose document (read with Docling).
RECORD_FILES = {"courses.docx", "discounts.docx", "company.docx"}


def read_table(path):
    doc = docx.Document(path)
    table = doc.tables[0]
    headers = [cell.text.strip() for cell in table.rows[0].cells]

    records = []
    for row in table.rows[1:]:
        values = [cell.text.strip() for cell in row.cells]
        if values[0]:
            records.append(dict(zip(headers, values)))
    return records


def extract_prose(path, converter):
    markdown = converter.convert(path).document.export_to_markdown()
    return [make_entry(1, markdown, "docling")]


def load_business(folder):
    folder = Path(folder)

    courses = read_table(folder / "courses.docx")
    discounts = read_table(folder / "discounts.docx")
    company_rows = read_table(folder / "company.docx")
    company = {row["field"]: row["value"] for row in company_rows}

    converter = DocumentConverter()
    documents = []
    for file in sorted(folder.glob("*.docx")):
        if file.name not in RECORD_FILES:
            documents.append({"file": file.name, "pages": extract_prose(file, converter)})

    return {
        "courses": courses,
        "discounts": discounts,
        "company": company,
        "documents": documents,
    }


if __name__ == "__main__":
    business = load_business("data/demo_academy")
    print("courses  :", len(business["courses"]))
    print("discounts:", len(business["discounts"]))
    print("company  :", business["company"])
    for d in business["documents"]:
        page = d["pages"][0]
        print(d["file"], page["method"], len(page["original_text"]), "characters")
