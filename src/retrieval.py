"""Top-k retrieval with current-policy priority."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class PolicyRetriever:
    def __init__(self, chunks):
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english"
        )

        self.matrix = (
            self.vectorizer.fit_transform([c["text"] for c in chunks])
            if chunks else None
        )

    def retrieve(self, question, k=3):
        if self.matrix is None:
            return []

        q = self.vectorizer.transform([question])
        scores = cosine_similarity(q, self.matrix).ravel()

        results = []

        for idx, score in enumerate(scores):
            if score <= 0:
                continue

            item = dict(self.chunks[idx])
            item["score"] = float(score)
            results.append(item)

        # Separate current and superseded policy results.
        current = [x for x in results if x.get("status") == "current"]
        superseded = [x for x in results if x.get("status") == "superseded"]

        current.sort(key=lambda x: x["score"], reverse=True)
        superseded.sort(key=lambda x: x["score"], reverse=True)

        # Prefer current policy results.
        ranked = current + superseded

        return ranked[:k]