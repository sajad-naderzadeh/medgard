class RAGSecurityGuard:

    INJECTION_PATTERNS = [
        "ignore previous instructions",
        "ignore system instructions",
        "follow these instructions",
        "execute this command",
        "reveal the system prompt",
        "disregard safety",
    ]

    def scan_document(self, text: str) -> dict:
        normalized = text.lower()

        detected = [
            pattern
            for pattern in self.INJECTION_PATTERNS
            if pattern in normalized
        ]

        return {
            "trusted": len(detected) == 0,
            "detected_patterns": detected,
        }

    def sanitize_context(
        self,
        documents: list[dict],
    ) -> list[dict]:
        safe_documents = []

        for document in documents:
            result = self.scan_document(
                document.get("text", "")
            )

            if result["trusted"]:
                safe_documents.append(document)

        return safe_documents
