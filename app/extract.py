from pypdf import PdfReader
from pathlib import Path
from PIL import Image
import pytesseract
import io

def extract_pdf(path):
    pdf = PdfReader(path)
    full_text = ""

    for index, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text.strip():
            if page.images:
                for img in page.images:
                    image = io.BytesIO(img.data)
                    pli_image = Image.open(image)
                    text = pytesseract.image_to_string(pli_image, lang="mal+eng")
                    full_text += text
            else:
                print(f"page{index + 1} has no content")
        else:
            full_text += text
    
    return full_text

result = extract_pdf("data/PSC Notification.pdf")
print(result[:200])

        
            



