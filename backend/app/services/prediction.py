from pathlib import Path

import pandas as pd

from app.models.prediction import PredictionRecord
from app.repositories.prediction import PredictionRepository
from ml.models.model_loader import ModelLoader
from ml.preprocessing.clinical_features import ClinicalFeatureEngineer
from ml.models.risk_score import RiskScore
from ml.models.risk_classification import RiskClassification


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = PROJECT_ROOT / "ml/models/artifacts/cardiovascular_logistic_regression.joblib"


class CardiovascularPredictionService:

    def __init__(self):
        self.loader = ModelLoader(str(MODEL_PATH))
        self.feature_engineer = ClinicalFeatureEngineer()
        self.repository = PredictionRepository()

    async def predict(
        self,
        data: dict,
        patient_id: str | None = None,
    ) -> dict:

        dataframe = pd.DataFrame([data])
        dataframe = self.feature_engineer.transform(dataframe)

        probability = self.loader.predict_probability(dataframe)

        risk_score = RiskScore.calculate(probability)
        risk_category = RiskClassification.classify(risk_score)

        result = {
            "probability": round(probability, 4),
            "risk_score": risk_score,
            "risk_category": risk_category,
            "model": "cardiovascular_logistic_regression",
            "disclaimer": (
                "Research prototype for clinical decision support. "
                "Not a diagnostic system."
            ),
        }

        if patient_id:
            record = PredictionRecord.build(
                patient_id=patient_id,
                probability=result["probability"],
                risk_score=risk_score,
                risk_category=risk_category,
                model=result["model"],
                input_features=data,
            )

            await self.repository.create(record)

        return result

    async def history(
        self,
        patient_id: str,
        limit: int = 50,
    ) -> list[dict]:
        return await self.repository.get_by_patient(
            patient_id,
            limit,
        )
