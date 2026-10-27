from ml.models.risk_score import RiskScore
from ml.models.risk_classification import RiskClassification


def test_risk_score():
    assert RiskScore.calculate(0.73) == 73.0


def test_risk_classification():
    assert RiskClassification.classify(10) == "low"
    assert RiskClassification.classify(30) == "moderate"
    assert RiskClassification.classify(60) == "high"
    assert RiskClassification.classify(90) == "very_high"
