from ml.models.cardiovascular import CardiovascularRiskModel
from ml.models.risk_score import RiskScore
from ml.models.risk_classification import RiskClassification
from ml.clinical.rules import ClinicalRuleEngine


class ClinicalDecisionSupport:
    def __init__(
        self,
        model_path: str = "ml/models/artifacts/model.joblib",
    ):
        self.model = CardiovascularRiskModel(model_path)
        self.rules = ClinicalRuleEngine()

    def assess(self, patient_features: dict) -> dict:
        prediction = self.model.predict(
            patient_features
        )

        probability = prediction["probability"]

        score = None
        classification = None

        if probability is not None:
            score = RiskScore.calculate(probability)
            classification = RiskClassification.classify(
                score
            )

        alerts = self.rules.evaluate(
            patient_features
        )

        return {
            "model": prediction["model"],
            "prediction": prediction["prediction"],
            "probability": probability,
            "risk_score": score,
            "risk_class": classification,
            "clinical_alerts": alerts,
            "disclaimer": (
                "This system provides clinical decision "
                "support and does not constitute a diagnosis."
            ),
        }
