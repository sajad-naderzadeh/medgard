from datetime import datetime, timezone


class ModelMonitor:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def record_prediction(
        self,
        prediction: int,
        probability: float | None,
    ) -> dict:
        return {
            "model_name": self.model_name,
            "prediction": prediction,
            "probability": probability,
            "timestamp": datetime.now(
                timezone.utc
            ),
        }
