class ModelHealth:

    def evaluate(
        self,
        metrics: dict,
        max_error_rate: float = 0.05,
        max_latency_ms: float = 1000.0,
    ) -> dict:

        issues = []

        if metrics["error_rate"] > max_error_rate:
            issues.append("high_error_rate")

        if metrics["average_latency_ms"] > max_latency_ms:
            issues.append("high_latency")

        return {
            "healthy": len(issues) == 0,
            "issues": issues,
        }
