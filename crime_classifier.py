# crime_classifier.py

import pandas as pd
import re
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Download NLTK stopwords if not already installed
nltk.download('stopwords')
from nltk.corpus import stopwords

# -------------------------
# 1. Load Dataset
# -------------------------
df = pd.read_csv("crime_dataset.csv")

# -------------------------
# 2. Preprocessing Function
# -------------------------
def preprocess_text(text):
    # Lowercase
    text = text.lower()
    # Remove numbers & special chars
    text = re.sub(r'[^a-z\s]', '', text)
    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = text.split()
    filtered_words = [w for w in words if w not in stop_words]
    return " ".join(filtered_words)

df["Clean_Text"] = df["FIR_Text"].apply(preprocess_text)

# -------------------------
# 3. TF-IDF Vectorization
# -------------------------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["Clean_Text"])

# Target Labels
y_type = df["Crime_Type"]      # Theft, Fraud, Murder, etc.
y_severity = df["Severity"]    # Low, Medium, High

# -------------------------
# 4. Train/Test Split
# -------------------------
X_train, X_test, y_type_train, y_type_test = train_test_split(X, y_type, test_size=0.2, random_state=42)
_, _, y_sev_train, y_sev_test = train_test_split(X, y_severity, test_size=0.2, random_state=42)

# -------------------------
# 5. Train Models
# -------------------------
crime_type_model = LogisticRegression(max_iter=200)
crime_type_model.fit(X_train, y_type_train)

severity_model = LogisticRegression(max_iter=200)
severity_model.fit(X_train, y_sev_train)

# -------------------------
# 6. Evaluate Models
# -------------------------
print("Crime Type Classification Report:\n", classification_report(y_type_test, crime_type_model.predict(X_test)))
print("Severity Classification Report:\n", classification_report(y_sev_test, severity_model.predict(X_test)))

# -------------------------
# 7. Save Models
# -------------------------
joblib.dump(crime_type_model, "models/crime_type_model.pkl")
joblib.dump(severity_model, "models/severity_model.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

print("✅ Models trained and saved successfully!")
