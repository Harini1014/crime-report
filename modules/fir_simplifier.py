import os
import traceback

# Try Gemini first
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Try Hugging Face summarizer
try:
    from transformers import pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    HF_AVAILABLE = True
except Exception:
    HF_AVAILABLE = False


def simplify_fir_text(text: str) -> str:
    """
    Simplifies or summarizes a given FIR/crime report text.
    Prefers Gemini if API key configured; otherwise uses HuggingFace.
    """
    if not text or text.strip() == "":
        return "❌ No text provided."

    try:
        # --- Option 1: Gemini AI (if available)
        if GEMINI_AVAILABLE and os.getenv("GEMINI_API_KEY"):
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel("gemini-pro")
            prompt = (
                "Simplify this FIR report into easy-to-understand English, "
                "keeping all important legal details:\n\n" + text
            )
            response = model.generate_content(prompt)
            return response.text.strip()

        # --- Option 2: Hugging Face summarization
        elif HF_AVAILABLE:
            summary = summarizer(text, max_length=180, min_length=60, do_sample=False)
            return summary[0]["summary_text"].strip()

        # --- Option 3: Fallback simple truncation
        else:
            simplified = " ".join(text.split()[:150])
            return simplified + "... (summary truncated - no AI model active)"

    except Exception as e:
        traceback.print_exc()
        return f"⚠️ Simplification failed: {str(e)}"
