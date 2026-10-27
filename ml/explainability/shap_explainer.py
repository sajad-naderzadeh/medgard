from pathlib import Path

import joblib
import pandas as pd
import shap


class CardiovascularSHAPExplainer:

    def __init__(self, model_path: str):
        self.model_path = Path(model_path)
        self.model = joblib.load(self.model_path)

    def explain(self, features: dict) -> list[dict]:
        dataframe = pd.DataFrame([features])

        if hasattr(self.model, "named_steps"):
            preprocessor = self.model.named_steps.get("preprocessor")
            classifier = self.model.named_steps.get("classifier")

            if preprocessor is not None:
                transformed = preprocessor.transform(dataframe)

                feature_names = preprocessor.get_feature_names_out()

                explainer = shap.LinearExplainer(
                    classifier,
                    transformed,
                )

                values = explainer.shap_values(transformed)

                if hasattr(values, "ndim") and values.ndim == 2:
                    values = values[0]

                result = [
                    {
                        "feature": str(name),
                        "impact": round(float(value), 6),
                    }
                    for name, value in zip(feature_names, values)
                ]

                result.sort(
                    key=lambda item: abs(item["impact"]),
                    reverse=True,
                )

                return result[:10]

        return []
