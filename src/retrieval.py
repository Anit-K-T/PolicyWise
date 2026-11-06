
from ingestion import VectorStore, get_embedder


class PolicyRetriever:
    """
    Semantic retrieval using the persisted FAISS/NumPy index.
    """

    def __init__(self, vector_store, embedder):
        self.vector_store = vector_store
        self.embedder = embedder

    def retrieve(self, question, k=3):
        if not question.strip():
            return []

        query_vector = self.embedder.encode([question])[0]

        hits = self.vector_store.search(
            query_vector,
            k=k
        )

        results = []

        for score, chunk in hits:
            item = dict(chunk)

            item["score"] = float(score)
            item["source"] = item["doc_name"]
            item["version"] = item.get("status", "unknown")

            results.append(item)

        return results
