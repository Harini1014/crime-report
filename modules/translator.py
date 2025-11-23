from langdetect import detect
from googletrans import Translator

google_translator = Translator()

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def translate_to_language(text, target_lang):
    if target_lang == "en":
        return text
    try:
        translated = google_translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        print(f"❌ Google Translate error: {e}")
        return "❌ Translation failed. Please try again later."