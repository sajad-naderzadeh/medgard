class AISecurityScanner:
    SUSPICIOUS_PATTERNS = [
        "ignore previous instructions",
        "ignore all instructions",
        "reveal system prompt",
        "show system prompt",
        "bypass safety",
        "disable safety",
        "jailbreak",
    ]

    def scan(self, text: str) -> dict:
        normalized = text.lower()

        detected = [
            pattern
            for pattern in self.SUSPICIOUS_PATTERNS
            if pattern in normalized
        ]

        return {
            "safe": len(detected) == 0,
            "detected_patterns": detected,
            "risk_level": (
                "high"
                if detected
                else "low"
            ),
        }
