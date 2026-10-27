from ml.embeddings.service import EmbeddingService
from ml.vector_store.store import LocalVectorStore


class HybridSearch:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: LocalVectorStore,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    @staticmethod
    def keyword_score(
        query: str,
        text: str,
    ) -> float:
        query_terms = set(
            query.lower().split()
        )

        text_terms = set(
            text.lower().split()
        )

        if not query_terms:
            return 0.0

        return len(
            query_terms.intersection(text_terms)
        ) / len(query_terms)

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        query_embedding = (
            self.embedding_service.embed(query)
        )

        vector_results = self.vector_store.search(
            query_embedding,
            top_k=max(top_k * 2, 10),
        )

        ranked = []

        for item in vector_results:
            keyword = self.keyword_score(
                query,
                item["text"],
            )

            vector_score = item["score"]

            final_score = (
                0.7 * vector_score
                + 0.3 * keyword
            )

            ranked.append(
                {
                    **item,
                    "keyword_score": keyword,
                    "vector_score": vector_score,
                    "final_score": final_score,
                }
            )

        ranked.sort(
            key=lambda item: item["final_score"],
            reverse=True,
        )

        return ranked[:top_k]
