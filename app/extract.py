import io
from pathlib import Path

import docx
import pymupdf
import pytesseract
from docx.table import Table
from docx.text.paragraph import Paragraph
from PIL import Image

from clean import normalize, match_key

# What every extractor returns: a list with one dictionary per page.
#   original_text : exactly what the extractor gave us, untouched
#   text          : normalize(original_text), readable, keeps line breaks and capitals
#   key           : match_key(original_text), used only for comparing, never shown


def make_entry(page_no, original_text, method):
    return {
        "page_no": page_no,
        "original_text": original_text,
        "text": normalize(original_text),
        "key": match_key(original_text),
        "method": method,
    }


def looks_garbled(text):
    for ch in text:
        if ord(ch) < 32 and ch not in "\n\t\r":
            return True
    return False


def ocr_image(image):
    return pytesseract.image_to_string(image, lang="mal+eng")


def ocr_page(page):
    pix = page.get_pixmap(dpi=300)
    image = Image.open(io.BytesIO(pix.tobytes("png")))
    return ocr_image(image)


def extract_pdf(path):
    doc = pymupdf.open(path)
    pages = []

    for page in doc:
        text = page.get_text()
        if text.strip() and not looks_garbled(text):
            method = "text"
        else:
            text = ocr_page(page)
            method = "ocr" if text.strip() else "empty"
        pages.append(make_entry(page.number + 1, text, method))

    doc.close()
    return pages


def table_to_text(table):
    lines = []
    for row in table.rows:
        cells = [cell.text.strip() for cell in row.cells]
        lines.append(" | ".join(cells))
    return "\n".join(lines)


def extract_docx(path):
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


def extract_image(path):
    with Image.open(path) as image:
        text = ocr_image(image)
    method = "ocr" if text.strip() else "empty"
    return [make_entry(1, text, method)]


READERS = {
    ".pdf": extract_pdf,
    ".docx": extract_docx,
    ".png": extract_image,
    ".jpg": extract_image,
    ".jpeg": extract_image,
}


def extract_document(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    extension = path.suffix.lower()
    reader = READERS.get(extension)
    if reader is None:
        supported = ", ".join(READERS)
        raise ValueError(f"Unsupported file type '{extension}'. Supported: {supported}")

    return reader(path)


if __name__ == "__main__":
    files = [
        "data/PSC Notification.pdf",
        "data/psc eng mal.pdf",
        "data/malayalam_manglish_english.pdf",
        "data/institute_sample.docx",
    ]
    for file in files:
        print("=====", file)
        for p in extract_document(file):
            print(p["page_no"], p["method"])
            print("  original:", repr(p["original_text"][:60]))
            print("  text    :", repr(p["text"][:60]))
            print("  key     :", repr(p["key"][:60]))