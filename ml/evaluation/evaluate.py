import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)


class ModelEvaluator:
    def evaluate(self, model, X_test, y_test) -> dict:
        predictions = model.predict(X_test)

        metrics = {
            "accuracy": accuracy_score(
                y_test,
                predictions,
            ),
            "precision": precision_score(
                y_test,
                predictions,
                zero_division=0,
            ),
            "recall": recall_score(
                y_test,
                predictions,
                zero_division=0,
            ),
            "f1": f1_score(
                y_test,
                predictions,
                zero_division=0,
            ),
        }

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(X_test)[:, 1]
            metrics["roc_auc"] = roc_auc_score(
                y_test,
                probabilities,
            )

        return metrics

    @staticmethod
    def to_dataframe(metrics: dict) -> pd.DataFrame:
        return pd.DataFrame(
            [metrics],
            index=["model"],
        )
