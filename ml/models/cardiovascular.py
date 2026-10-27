from pathlib import Path

from ml.services import PredictionService


class CardiovascularRiskModel:
    MODEL_NAME = "MedGuard Cardiovascular Risk Model"

    def __init__(
        self,
        model_path: str = "ml/models/artifacts/model.joblib",
    ):
        self.predictor = PredictionService(model_path)

    def predict(self, patient_features: dict) -> dict:
        result = self.predictor.predict(patient_features)

        return {
            "model": self.MODEL_NAME,
            "prediction": result["prediction"],
            "probability": result["probability"],
        }
