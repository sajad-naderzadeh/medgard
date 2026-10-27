from ml.models.risk_score import RiskScore
from ml.models.risk_classification import RiskClassification
from ml.clinical.rules import ClinicalRuleEngine
from ml.safety.guardrails import MedicalSafetyGuardrails


def test_medguard_end_to_end():

    probability = 0.65

    score = RiskScore.calculate(
        probability
    )

    risk_class = RiskClassification.classify(
        score
    )

    alerts = ClinicalRuleEngine().evaluate(
        {
            "systolic_bp": 130,
            "oxygen_saturation": 97,
        }
    )

    guardrails = MedicalSafetyGuardrails()

    safety = guardrails.validate_question(
        "What does cardiovascular risk mean?"
    )

    assert score == 65.0
    assert risk_class == "high"
    assert alerts == []
    assert safety["safe"] is True
