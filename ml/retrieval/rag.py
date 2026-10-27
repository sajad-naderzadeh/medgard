from ml.retrieval.hybrid_search import HybridSearch


class RAGPipeline:
    def __init__(
        self,
        search_engine: HybridSearch,
    ):
        self.search_engine = search_engine

    def retrieve(
        self,
        question: str,
        top_k: int = 5,
    ) -> list[dict]:
        return self.search_engine.search(
            question,
            top_k=top_k,
        )

    def build_context(
        self,
        results: list[dict],
    ) -> str:
        context_parts = []

        for index, result in enumerate(results, 1):
            context_parts.append(
                f"[Source {index}] "
                f"{result['text']}"
            )

        return "\n\n".join(
            context_parts
        )

    def prepare(
        self,
        question: str,
        top_k: int = 5,
    ) -> dict:
        results = self.retrieve(
            question,
            top_k,
        )

        return {
            "question": question,
            "context": self.build_context(results),
            "sources": [
                {
                    "document_id": item["document_id"],
                    "score": item["final_score"],
                    "metadata": item["metadata"],
                }
                for item in results
            ],
        }
