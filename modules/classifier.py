import joblib

# Load models
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
crime_type_model = joblib.load("models/crime_type_model.pkl")
severity_model = joblib.load("models/severity_model.pkl")

def predict_crime(fir_text):
    X_new = vectorizer.transform([fir_text])
    crime_type = crime_type_model.predict(X_new)[0]
    severity = severity_model.predict(X_new)[0]
    return crime_type, severity