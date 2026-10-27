class RiskClassification:
    LOW_THRESHOLD = 20
    MODERATE_THRESHOLD = 50
    HIGH_THRESHOLD = 75

    @classmethod
    def classify(cls, score: float) -> str:
        if score < cls.LOW_THRESHOLD:
            return "low"

        if score < cls.MODERATE_THRESHOLD:
            return "moderate"

        if score < cls.HIGH_THRESHOLD:
            return "high"

        return "very_high"
