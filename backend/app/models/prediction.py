from datetime import datetime, timezone
from typing import Any


class PredictionRecord:
    @staticmethod
    def build(
        patient_id: str,
        probability: float,
        risk_score: float,
        risk_category: str,
        model: str,
        input_features: dict[str, Any],
    ) -> dict:
        return {
            "patient_id": patient_id,
            "probability": probability,
            "risk_score": risk_score,
            "risk_category": risk_category,
            "model": model,
            "input_features": input_features,
            "created_at": datetime.now(timezone.utc),
        }
