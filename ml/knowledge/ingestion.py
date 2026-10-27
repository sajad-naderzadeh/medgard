from pathlib import Path

from ml.knowledge.base import (
    KnowledgeDocument,
    MedicalKnowledgeBase,
)


class DocumentIngestion:
    def __init__(self, knowledge_base: MedicalKnowledgeBase):
        self.knowledge_base = knowledge_base

    def ingest_text(
        self,
        path: str,
        title: str,
        source: str,
        category: str,
    ) -> KnowledgeDocument:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        content = file_path.read_text(
            encoding="utf-8"
        )

        document = KnowledgeDocument(
            document_id=file_path.stem,
            title=title,
            content=content,
            source=source,
            category=category,
        )

        self.knowledge_base.add_document(document)

        return document
