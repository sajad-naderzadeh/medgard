class ClinicalRuleEngine:

    def evaluate(self, patient: dict) -> list[dict]:
        alerts = []

        systolic = patient.get("systolic_bp")

        if systolic is not None and systolic >= 180:
            alerts.append(
                {
                    "rule": "SEVERE_HYPERTENSION_ALERT",
                    "severity": "critical",
                    "message": (
                        "Systolic blood pressure is "
                        "markedly elevated."
                    ),
                }
            )

        oxygen = patient.get("oxygen_saturation")

        if oxygen is not None and oxygen < 90:
            alerts.append(
                {
                    "rule": "LOW_OXYGEN_SATURATION",
                    "severity": "critical",
                    "message": (
                        "Oxygen saturation is "
                        "markedly low."
                    ),
                }
            )

        return alerts
