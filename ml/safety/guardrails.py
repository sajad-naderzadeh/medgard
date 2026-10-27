class MedicalSafetyGuardrails:

    HIGH_RISK_TERMS = {
        "diagnose",
        "diagnosis",
        "prescribe",
        "prescription",
        "emergency",
        "suicide",
        "overdose",
    }

    def validate_question(
        self,
        question: str,
    ) -> dict:
        normalized = question.lower()

        detected = [
            term
            for term in self.HIGH_RISK_TERMS
            if term in normalized
        ]

        return {
            "safe": len(detected) == 0,
            "risk_terms": detected,
        }

    def validate_answer(
        self,
        answer: str,
        sources: list[dict],
    ) -> dict:
        has_sources = len(sources) > 0

        return {
            "grounded": has_sources,
            "requires_review": not has_sources,
            "disclaimer": (
                "MedGuard AI provides clinical decision "
                "support and does not replace a qualified "
                "healthcare professional."
            ),
        }

    def guard(
        self,
        question: str,
        answer: str,
        sources: list[dict],
    ) -> dict:
        question_check = self.validate_question(
            question
        )

        answer_check = self.validate_answer(
            answer,
            sources,
        )

        return {
            "question_safe": question_check["safe"],
            "risk_terms": question_check["risk_terms"],
            "grounded": answer_check["grounded"],
            "requires_review": (
                answer_check["requires_review"]
            ),
            "disclaimer": answer_check["disclaimer"],
        }
