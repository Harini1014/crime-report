import os
import google.generativeai as genai

# Set your Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyDLFdY5nhtiQS6s6ZtVOPfSRK0M88Kc9TA")
genai.configure(api_key=GEMINI_API_KEY)

try:
    models = genai.list_models()
    print("✅ Available Gemini Models:")
    for model in models:
        print(f"- {model.name}")
except Exception as e:
    print(f"❌ Error while listing models: {e}")