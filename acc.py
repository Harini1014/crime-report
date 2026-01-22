import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# -----------------------------
# Load Dataset (force header)
# -----------------------------
df = pd.read_csv("crime_dataset.csv", header=0)

# Clean column names
df.columns = df.columns.str.strip().str.replace('\ufeff', '')

print("Loaded columns:", df.columns.tolist())

# Auto-fix if first row was treated as header
if "FIR_Text" not in df.columns:
    df.rename(columns={
        df.columns[0]: "FIR_Text",
        df.columns[1]: "Crime_Type",
        df.columns[2]: "Severity"
    }, inplace=True)
    print("Fixed column names:", df.columns.tolist())

X = df["FIR_Text"]
y_type = df["Crime_Type"]
y_sev = df["Severity"]

# -----------------------------
# Vectorize Text
# -----------------------------
vectorizer = TfidfVectorizer(stop_words="english")
X_vec = vectorizer.fit_transform(X)

# -----------------------------
# Train-Test Split
# -----------------------------
X_train, X_test, y_type_train, y_type_test = train_test_split(
    X_vec, y_type, test_size=0.2, random_state=42
)

X_train_s, X_test_s, y_sev_train, y_sev_test = train_test_split(
    X_vec, y_sev, test_size=0.2, random_state=42
)

# -----------------------------
# Train Crime-Type Model
# -----------------------------
type_model = RandomForestClassifier(n_estimators=200, random_state=42)
type_model.fit(X_train, y_type_train)
y_type_pred = type_model.predict(X_test)
type_acc = accuracy_score(y_type_test, y_type_pred)

# -----------------------------
# Train Severity Model
# -----------------------------
sev_model = RandomForestClassifier(n_estimators=200, random_state=42)
sev_model.fit(X_train_s, y_sev_train)
y_sev_pred = sev_model.predict(X_test_s)
sev_acc = accuracy_score(y_sev_test, y_sev_pred)

# -----------------------------
# Save Models
# -----------------------------
os.makedirs("models", exist_ok=True)
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")
joblib.dump(type_model, "models/crime_type_model.pkl")
joblib.dump(sev_model, "models/severity_model.pkl")

# -----------------------------
# Print Final Accuracies ONLY
# -----------------------------
print("\n🎯 Model Training Completed!")
print(f"🔍 Crime-Type Accuracy: {round(type_acc * 100, 2)}%")
print(f"⚠️ Severity Accuracy:  {round(sev_acc * 100, 2)}%\n")
