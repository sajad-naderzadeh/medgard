from ml.models.risk_score import RiskScore
from ml.models.risk_classification import RiskClassification
from ml.clinical.rules import ClinicalRuleEngine


def test_clinical_pipeline():

    probability = 0.73

    score = RiskScore.calculate(
        probability
    )

    classification = RiskClassification.classify(
        score
    )

    alerts = ClinicalRuleEngine().evaluate(
        {
            "systolic_bp": 185,
            "oxygen_saturation": 88,
        }
    )

    assert score == 73.0
    assert classification == "high"
    assert len(alerts) == 2
