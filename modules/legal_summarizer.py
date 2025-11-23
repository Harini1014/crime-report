import traceback

try:
    from transformers import pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    MODEL_AVAILABLE = True
except Exception:
    MODEL_AVAILABLE = False

def summarize_legal_text(text: str) -> str:
    """
    Summarizes legal or crime text into concise form.
    """
    if not text or text.strip() == "":
        return "❌ Empty text provided for summarization."

    try:
        if MODEL_AVAILABLE:
            summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
            return summary[0]['summary_text'].strip()
        else:
            # fallback
            return " ".join(text.split()[:100]) + "... (summary truncated - model not loaded)"

    except Exception as e:
        traceback.print_exc()
        return f"⚠️ Summarization failed: {str(e)}"
