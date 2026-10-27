from datetime import datetime, timezone


class ProductionMetrics:
    def __init__(self):
        self.predictions = 0
        self.errors = 0
        self.total_latency_ms = 0.0

    def record_prediction(
        self,
        latency_ms: float,
    ) -> None:
        self.predictions += 1
        self.total_latency_ms += latency_ms

    def record_error(self) -> None:
        self.errors += 1

    def snapshot(self) -> dict:
        average_latency = (
            self.total_latency_ms / self.predictions
            if self.predictions
            else 0.0
        )

        error_rate = (
            self.errors / self.predictions
            if self.predictions
            else 0.0
        )

        return {
            "predictions": self.predictions,
            "errors": self.errors,
            "error_rate": round(error_rate, 4),
            "average_latency_ms": round(
                average_latency,
                2,
            ),
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
        }
