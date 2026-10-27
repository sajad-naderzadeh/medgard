from ml.retrieval.rag import RAGPipeline


class MedicalQASystem:
    def __init__(
        self,
        rag_pipeline: RAGPipeline,
        llm=None,
    ):
        self.rag = rag_pipeline
        self.llm = llm

    def answer(self, question: str) -> dict:
        rag_result = self.rag.prepare(question)

        if self.llm is None:
            answer = (
                "No local language model is configured. "
                "Retrieved medical context is available "
                "for downstream generation."
            )
        else:
            answer = self.llm.generate(
                question=question,
                context=rag_result["context"],
            )

        return {
            "question": question,
            "answer": answer,
            "sources": rag_result["sources"],
        }
