import math


class LocalVectorStore:
    def __init__(self):
        self.items: list[dict] = []

    def add(
        self,
        document_id: str,
        text: str,
        embedding: list[float],
        metadata: dict | None = None,
    ) -> None:
        self.items.append(
            {
                "document_id": document_id,
                "text": text,
                "embedding": embedding,
                "metadata": metadata or {},
            }
        )

    @staticmethod
    def cosine_similarity(
        a: list[float],
        b: list[float],
    ) -> float:
        dot = sum(
            x * y for x, y in zip(a, b)
        )

        norm_a = math.sqrt(
            sum(x * x for x in a)
        )

        norm_b = math.sqrt(
            sum(y * y for y in b)
        )

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot / (norm_a * norm_b)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[dict]:
        results = []

        for item in self.items:
            score = self.cosine_similarity(
                query_embedding,
                item["embedding"],
            )

            results.append(
                {
                    **item,
                    "score": score,
                }
            )

        results.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return results[:top_k]
