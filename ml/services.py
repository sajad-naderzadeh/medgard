from pathlib import Path
import joblib
import pandas as pd


class PredictionService:
    def __init__(
        self,
        model_path: str = "ml/models/artifacts/model.joblib",
    ):
        self.model_path = Path(model_path)
        self.model = None

    def load_model(self):
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {self.model_path}"
            )

        self.model = joblib.load(self.model_path)
        return self.model

    def predict(self, features: dict) -> dict:
        if self.model is None:
            self.load_model()

        df = pd.DataFrame([features])

        prediction = self.model.predict(df)[0]

        probability = None
        if hasattr(self.model, "predict_proba"):
            probability = float(
                self.model.predict_proba(df)[0][1]
            )

        return {
            "prediction": int(prediction),
            "probability": probability,
        }
