import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold

from ml.training.benchmark import ModelBenchmark


RANDOM_STATE = 42
N_SPLITS = 5


BEST_PARAMS = {
    "C": 0.1,
    "class_weight": "balanced",
    "solver": "liblinear",
}


class FinalModelSelector:

    def __init__(
        self,
        dataset_path: str,
    ):
        self.dataset_path = dataset_path

        self.benchmark = ModelBenchmark(
            dataset_path=dataset_path
        )

    @staticmethod
    def calculate_metrics(
        y_true,
        probabilities,
        threshold=0.5,
    ):
        predictions = (
            probabilities >= threshold
        ).astype(int)

        tn, fp, fn, tp = confusion_matrix(
            y_true,
            predictions,
            labels=[0, 1],
        ).ravel()

        specificity = (
            tn / (tn + fp)
            if (tn + fp) > 0
            else 0.0
        )

        return {
            "roc_auc": roc_auc_score(
                y_true,
                probabilities,
            ),
            "pr_auc": average_precision_score(
                y_true,
                probabilities,
            ),
            "accuracy": accuracy_score(
                y_true,
                predictions,
            ),
            "precision": precision_score(
                y_true,
                predictions,
                zero_division=0,
            ),
            "recall": recall_score(
                y_true,
                predictions,
                zero_division=0,
            ),
            "specificity": specificity,
            "f1": f1_score(
                y_true,
                predictions,
                zero_division=0,
            ),
        }

    def build_model(self):
        return LogisticRegression(
            C=BEST_PARAMS["C"],
            class_weight=BEST_PARAMS["class_weight"],
            solver=BEST_PARAMS["solver"],
            max_iter=3000,
            random_state=RANDOM_STATE,
        )

    def cross_validate(self):

        X, y = self.benchmark.load_data()

        cv = StratifiedKFold(
            n_splits=N_SPLITS,
            shuffle=True,
            random_state=RANDOM_STATE,
        )

        fold_results = []

        for fold, (
            train_idx,
            test_idx,
        ) in enumerate(
            cv.split(X, y),
            start=1,
        ):

            X_train = X.iloc[train_idx]
            X_test = X.iloc[test_idx]

            y_train = y.iloc[train_idx]
            y_test = y.iloc[test_idx]

            model = self.build_model()

            pipeline = self.benchmark.build_pipeline(
                model
            )

            pipeline.fit(
                X_train,
                y_train,
            )

            probabilities = pipeline.predict_proba(
                X_test
            )[:, 1]

            metrics = self.calculate_metrics(
                y_test,
                probabilities,
            )

            metrics["fold"] = fold

            fold_results.append(metrics)

        results = pd.DataFrame(
            fold_results
        )

        summary = {}

        for metric in [
            "roc_auc",
            "pr_auc",
            "accuracy",
            "precision",
            "recall",
            "specificity",
            "f1",
        ]:
            summary[metric] = {
                "mean": float(
                    results[metric].mean()
                ),
                "std": float(
                    results[metric].std()
                ),
            }

        return results, summary

    def train_final_model(self):

        X, y = self.benchmark.load_data()

        model = self.build_model()

        pipeline = self.benchmark.build_pipeline(
            model
        )

        pipeline.fit(
            X,
            y,
        )

        artifacts_dir = Path(
            "ml/models/artifacts"
        )

        artifacts_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        model_path = (
            artifacts_dir
            / "cardiovascular_logistic_regression.joblib"
        )

        metadata_path = (
            artifacts_dir
            / "cardiovascular_model_metadata.json"
        )

        joblib.dump(
            pipeline,
            model_path,
        )

        metadata = {
            "model_name": "cardiovascular_logistic_regression",
            "algorithm": "LogisticRegression",
            "dataset": self.dataset_path,
            "dataset_rows": int(len(X)),
            "target": "condition",
            "random_state": RANDOM_STATE,
            "cross_validation_folds": N_SPLITS,
            "hyperparameters": BEST_PARAMS,
            "clinical_note": (
                "Research prototype for clinical decision support. "
                "Not a diagnostic system."
            ),
        }

        with open(
            metadata_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                metadata,
                file,
                indent=2,
            )

        return model_path, metadata_path


if __name__ == "__main__":

    selector = FinalModelSelector(
        dataset_path=(
            "datasets/raw/"
            "heart_cleveland_upload.csv"
        )
    )

    print("\n")
    print("=" * 80)
    print("FINAL MODEL CROSS-VALIDATION")
    print("=" * 80)

    fold_results, summary = (
        selector.cross_validate()
    )

    print("\nFOLD RESULTS:")
    print(
        fold_results.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    print("\nSUMMARY:")
    print("-" * 80)

    for metric, values in summary.items():
        print(
            f"{metric:15s}: "
            f"{values['mean']:.4f} "
            f"+/- "
            f"{values['std']:.4f}"
        )

    model_path, metadata_path = (
        selector.train_final_model()
    )

    print("\n")
    print("=" * 80)
    print("FINAL MODEL TRAINED")
    print("=" * 80)

    print(f"MODEL:    {model_path}")
    print(f"METADATA: {metadata_path}")
