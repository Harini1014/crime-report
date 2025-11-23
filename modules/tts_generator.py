from gtts import gTTS
import os

def text_to_speech(text, lang='en', filename='output.mp3'):
    """
    Converts text to speech using gTTS and saves it in static/ folder.
    Returns the saved filename (with path).
    """
    try:
        if not text or text.strip() == "":
            raise ValueError("Empty text provided for TTS")

        # Ensure 'static' directory exists
        static_dir = os.path.join(os.getcwd(), "static")
        os.makedirs(static_dir, exist_ok=True)

        # Construct output file path
        output_path = os.path.join(static_dir, filename)

        # Create TTS object
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_path)

        print(f"[INFO] Audio saved at: {output_path}")
        return output_path

    except Exception as e:
        print(f"[ERROR] TTS failed: {e}")
        return None
