from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textstat

def evaluate_simplification(original, simplified):
    # 1️⃣ Cosine similarity
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([original, simplified])
    cos_sim = cosine_similarity(vectors)[0][1]

    # 2️⃣ Crime keyword retention
    keywords = ["complainant", "police", "fir", "investigation", "stolen",
                "value", "items", "suspect", "crime", "mobile", "laptop"]

    original_cnt = sum(1 for k in keywords if k.lower() in original.lower())
    simplified_cnt = sum(1 for k in keywords if k.lower() in simplified.lower())
    keyword_retention = simplified_cnt / original_cnt if original_cnt != 0 else 0

    # 3️⃣ Compression ratio
    compression_ratio = len(simplified) / len(original)

    # 4️⃣ Readability improvement
    orig_read = textstat.flesch_reading_ease(original)
    simp_read = textstat.flesch_reading_ease(simplified)

    # 5️⃣ Final accuracy score
    accuracy = (cos_sim * 0.4) + (keyword_retention * 0.4) + ((1 - compression_ratio) * 0.2)

    return {
        "cosine_similarity": round(cos_sim, 3),
        "keyword_retention": round(keyword_retention, 3),
        "compression_ratio": round(compression_ratio, 3),
        "readability_original": round(orig_read, 2),
        "readability_simplified": round(simp_read, 2),
        "accuracy_score": round(accuracy * 100, 2)
    }
