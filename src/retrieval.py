"""Top-k retrieval with TF-IDF, with current-policy preference for relevant policy variants."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class PolicyRetriever:
    def __init__(self, chunks):
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words="english")
        self.matrix = self.vectorizer.fit_transform([c["text"] for c in chunks]) if chunks else None

    def retrieve(self, question, k=3):
        if self.matrix is None: return []
        q = self.vectorizer.transform([question])
        scores = cosine_similarity(q, self.matrix).ravel()
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        # Prefer current over superseded when score is reasonably close, not at expense of relevance.
        top = []
        for idx, score in ranked:
            if score <= 0: continue
            item = dict(self.chunks[idx], score=float(score))
            top.append(item)
        if not top: return []
        best = top[0]["score"]
        eligible = [x for x in top if x["score"] >= best * 0.72]
        eligible.sort(key=lambda x: (x["version"] == "current", x["score"]), reverse=True)
        selected = eligible[:k]
        if len(selected) < k:
            for item in top:
                if item not in selected:
                    selected.append(item)
                if len(selected) == k: break
        return selected[:k]
