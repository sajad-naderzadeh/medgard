from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class KnowledgeDocument:
    document_id: str
    title: str
    content: str
    source: str
    category: str
    version: str = "1.0"

    def to_dict(self) -> dict:
        return {
            "document_id": self.document_id,
            "title": self.title,
            "content": self.content,
            "source": self.source,
            "category": self.category,
            "version": self.version,
            "created_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }


class MedicalKnowledgeBase:
    def __init__(self):
        self.documents: dict[str, KnowledgeDocument] = {}

    def add_document(
        self,
        document: KnowledgeDocument,
    ) -> None:
        self.documents[document.document_id] = document

    def get_document(
        self,
        document_id: str,
    ) -> KnowledgeDocument | None:
        return self.documents.get(document_id)

    def list_documents(self) -> list[KnowledgeDocument]:
        return list(self.documents.values())
