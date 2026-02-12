from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
import traceback
UPLOAD_FOLDER = 'uploads'
STATIC_AUDIO_FOLDER = os.path.join('static')  # audio saved inside static so templates can serve it
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXT = {'.pdf', '.png', '.jpg', '.jpeg', '.txt', '.mp3', '.wav'}

# If you don't want key-term explanations shown, set to False
ENABLE_TERM_EXPLANATIONS = False

# ---- App init ----
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_AUDIO_FOLDER, exist_ok=True)

# ---- Import modules safely ----
# Some modules (HuggingFace, Gemini, model files) may not be available in dev machine.
# We import and handle missing modules inside try/except blocks in the functions below where needed.
from modules.ocr_extractor import extract_text
from modules.fir_simplifier import simplify_fir_text
from modules.translator import translate_to_language, detect_language
from modules.tts_generator import text_to_speech
from modules.outcome_predictor import predict_outcome
from modules.classifier import predict_crime
from modules.ipc_explainer import extract_ipc_sections, load_ipc_data
from modules.dictionary_helper import get_word_meaning
from modules.legal_summarizer import summarize_legal_text
# legal_dictionary.explain_terms is optional
try:
    from modules.legal_dictionary import explain_terms
    HAS_EXPLAIN_TERMS = True
except Exception:
    HAS_EXPLAIN_TERMS = False


# ---- Helpers ----
def allowed_file(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXT

def safe_remove(path):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


# ---- Routes ----
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filepath = None
        try:
            # Validate file
            if 'fir_file' not in request.files:
                return render_template('result.html', error="❌ No file uploaded.")

            file = request.files['fir_file']
            user_language = request.form.get("language", "en") or "en"

            if not file or file.filename == '':
                return render_template('result.html', error="❌ No file selected.")

            if not allowed_file(file.filename):
                return render_template('result.html', error="❌ Unsupported file type.")

            # Save uploaded file
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # 1) OCR / Text extraction
            extracted_text = extract_text(filepath)
            if not extracted_text or not extracted_text.strip() or extracted_text.startswith("❌"):
                return render_template('result.html', error="❌ Could not extract text from the uploaded file. Please try a clearer scan or use a text file.")

            # 2) Simplify FIR text (Gemini / fallback message)
            simplified_text = simplify_fir_text(extracted_text)
            if not simplified_text:
                simplified_text = "⚠️ Simplification unavailable."

            # 3) Translate if requested (and not English)
            translated_text = None
            try:
                if user_language != 'en' and not simplified_text.startswith(("❌", "⚠️")):
                    # translate simplified_text into requested language
                    translated_text = translate_to_language(simplified_text, user_language)
                    # translator returns text or a failure message starting with ❌
                else:
                    # If user requested English or simplified_text is not valid, we keep translated_text None
                    translated_text = None
            except Exception as e:
                # don't crash translation: log and continue
                print("❌ Translation error:", e)
                translated_text = None

            # 4) Summarize legal text (use full extracted_text to preserve details)
            try:
                summary = summarize_legal_text(extracted_text)
            except Exception as e:
                print("⚠️ Summarization error:", e)
                summary = "⚠️ Summarization unavailable."

            # 5) Term explanations (optional toggle)
            term_explanations = {}
            if ENABLE_TERM_EXPLANATIONS and HAS_EXPLAIN_TERMS:
                try:
                    term_explanations = explain_terms(extracted_text)
                except Exception as e:
                    print("⚠️ explain_terms error:", e)
                    term_explanations = {}
            else:
                term_explanations = {}

            # 6) Crime classification (safe)
            try:
                crime_type, severity = predict_crime(simplified_text)
            except Exception as e:
                print("⚠️ crime classification error:", e)
                crime_type, severity = ("Unknown", "Unknown")

            # 7) Outcome prediction (rule based)
            try:
                crime_outcome = predict_outcome(simplified_text)
            except Exception as e:
                print("⚠️ outcome predictor error:", e)
                crime_outcome = "Outcome unavailable."

            # 8) Extract IPC sections
            try:
                ipc_results = extract_ipc_sections(extracted_text)
            except Exception as e:
                print("⚠️ ipc extraction error:", e)
                ipc_results = []

            # 9) Generate audio for the translated text if present else for simplified_text
            audio_file = None
            try:
                text_for_tts = translated_text if translated_text else simplified_text
                # ensure text_for_tts is not an error message
                if text_for_tts and not text_for_tts.startswith(("❌", "⚠️")):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    out_filename = f"output_fir_{timestamp}.mp3"
                    saved_filename = text_to_speech(text_for_tts, lang=user_language, filename=out_filename)
                    # text_to_speech should save into static/ and return filename or full path
                    # If tts returns full path, get basename for url_for
                    if saved_filename:
                        audio_file = os.path.basename(saved_filename)
            except Exception as e:
                print("⚠️ TTS error:", e)
                audio_file = None

            # Cleanup uploaded file (we keep audio)
            safe_remove(filepath)
            filepath = None

            return render_template(
                "result.html",
                extracted_text=extracted_text,
                simplified_text=simplified_text,
                translated_text=translated_text,
                user_language=user_language,
                audio_file=audio_file,
                crime_type=crime_type,
                severity=severity,
                crime_outcome=crime_outcome,
                ipc_results=ipc_results,
                summary=summary,
                term_explanations=term_explanations,
                error=None
            )

        except Exception as e:
            traceback.print_exc()
            # try to remove file if it was saved
            if filepath:
                safe_remove(filepath)
            return render_template('result.html', error=f"⚠️ Internal Error: {str(e)}")

    # GET
    return render_template('index.html')


@app.route('/define_word', methods=['POST'])
def define_word():
    word = request.form.get('word', '').strip()
    user_language = request.form.get('language', 'en') or 'en'
    if not word:
        return jsonify({'error': 'No word provided'})
    try:
        meaning = get_word_meaning(word)
    except Exception as e:
        print("⚠️ dictionary_helper error:", e)
        meaning = "Meaning not found."

    # translate meaning if requested and a translator is available
    if user_language != 'en' and meaning and meaning != "Meaning not found.":
        try:
            translated_meaning = translate_to_language(meaning, user_language)
            if translated_meaning and not translated_meaning.startswith("❌"):
                meaning = translated_meaning
        except Exception as e:
            print("⚠️ meaning translation error:", e)

    return jsonify({'meaning': meaning})


@app.route('/get_ipc_details', methods=['POST'])
def get_ipc_details():
    ipc_section = request.form.get('ipc_section', '').strip().upper().replace("IPC ", "")
    if not ipc_section:
        return jsonify({'error': 'No IPC section provided'})

    try:
        ipc_data = load_ipc_data()
    except Exception as e:
        print("⚠️ load_ipc_data error:", e)
        return jsonify({'error': 'IPC data not available on server'})

    if ipc_section in ipc_data:
        details = ipc_data[ipc_section]
        return jsonify({
            'section': f"IPC {ipc_section}",
            'description': details.get('description', 'No description available'),
            'punishment': details.get('punishment', 'No punishment available')
        })

    return jsonify({'error': 'IPC section not found'})


if __name__ == '__main__':
    # You can disable debug when deploying
    app.run(host='0.0.0.0', port=5001, debug=True)
