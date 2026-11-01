from pypdf import PdfReader
from pathlib import Path
from PIL import Image
import pytesseract
import io


def normalize(text):
    CHILLU_MAP = {
        "\u0d23\u0d4d\u200d": "\u0d7a",  # ണ് + ZWJ  ->  ൺ
        "\u0d28\u0d4d\u200d": "\u0d7b",  # ന് + ZWJ  ->  ൻ
        "\u0d30\u0d4d\u200d": "\u0d7c",  # ര് + ZWJ  ->  ർ
        "\u0d32\u0d4d\u200d": "\u0d7d",  # ല് + ZWJ  ->  ൽ
        "\u0d33\u0d4d\u200d": "\u0d7e",  # ള് + ZWJ  ->  ൾ
        "\u0d15\u0d4d\u200d": "\u0d7f",  # ക് + ZWJ  ->  ൿ
    }

    for key, value in CHILLU_MAP.items():
        text = text.replace(key, value)

    

    return text


def extract_pdf(path):
    pdf = PdfReader(path)
    full_text = []
    text_log = {}
    

    for index, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text.strip():
            if page.images:
                img_text = ""
                for img in page.images:
                    image = io.BytesIO(img.data)
                    pli_image = Image.open(image)
                    ocr_text = pytesseract.image_to_string(pli_image, lang="mal+eng")
                    img_text += ocr_text
                cleaned_text = normalize(img_text)
                text_log = {"page_no": index + 1, "text": cleaned_text, "method": "OCR"}
                full_text.append(text_log)
            else:
                print(f"page{index + 1} has no content")
                text_log = {"page_no": index + 1, "text": "", "method": "empty"}
                full_text.append(text_log)
        else:
            cleaned_text = normalize(text)
            text_log = {"page_no": index + 1, "text": cleaned_text, "method": "text"}
            full_text.append(text_log)
    
    return full_text

result = extract_pdf("data/psc eng mal.pdf")
for i in result:
    print(i)




