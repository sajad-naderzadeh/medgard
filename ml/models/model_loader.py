from pathlib import Path

import joblib


class ModelLoader:
    """Load and cache the trained cardiovascular model."""

    def __init__(self, model_path: str):
        self.model_path = Path(model_path)
        self._model = None

    def load(self):
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model artifact not found: {self.model_path}"
            )

        if self._model is None:
            self._model = joblib.load(self.model_path)

        return self._model

    def predict_probability(self, features):
        model = self.load()

        probabilities = model.predict_proba(features)

        return float(probabilities[0][1])

    def is_loaded(self) -> bool:
        return self._model is not None
