# modules/text_to_speech.py
from gtts import gTTS

def generate_audio(text, lang="en", filename="static/simplified_fir.mp3"):
    """
    Convert text to speech in the given language and save as mp3.
    """
    if not text:
        raise ValueError("No text provided for audio generation.")

    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    return filename
