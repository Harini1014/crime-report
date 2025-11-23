import pytesseract
from PIL import Image
import pdfplumber
import os
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Set Tesseract path (adjust for your OS)
pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH", r"C:\Program Files\Tesseract-OCR\tesseract.exe")
os.environ['TESSDATA_PREFIX'] = os.getenv("TESSDATA_PREFIX", r"C:\Program Files\Tesseract-OCR\tessdata")

def extract_text_from_image(image_path):
    try:
        with Image.open(image_path) as image:
            text = pytesseract.image_to_string(image, lang='eng').strip()
        return text if text else "⚠️ No text detected in the image."
    except Exception as e:
        return f"❌ Error in OCR (image): {e}"

def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    # Fallback for scanned PDFs
                    img = page.to_image()
                    text += pytesseract.image_to_string(img.original, lang='eng').strip() + "\n"
        return text.strip() if text.strip() else "⚠️ No text found in PDF pages."
    except Exception as e:
        return f"❌ Error in OCR (PDF): {e}"

def extract_text_from_txt(txt_path):
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        return text if text else "⚠️ Text file is empty."
    except Exception as e:
        return f"❌ Error reading text file: {e}"

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(file_path)
    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    return "❌ Unsupported file format"