import pdfplumber
from PIL import Image
import pytesseract
from pathlib import Path

def extract_text_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def ocr_image(path: str) -> str:
    img = Image.open(path)
    return pytesseract.image_to_string(img)

def extract_text(path: str) -> str:
    p = Path(path)
    if p.suffix.lower() in [".pdf"]:
        return extract_text_pdf(path)
    elif p.suffix.lower() in [".txt"]:
        return p.read_text(encoding='utf-8')
    else:
        return ocr_image(path)
