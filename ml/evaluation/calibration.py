import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.calibration import calibration_curve
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from ml.training.benchmark import ModelBenchmark


RANDOM_STATE = 42
N_SPLITS = 5


class ModelCalibration:

    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path

        self.benchmark = ModelBenchmark(
            dataset_path=dataset_path
        )

    def build_model(self):
        return LogisticRegression(
            C=0.1,
            class_weight="balanced",
            solver="liblinear",
            max_iter=3000,
            random_state=RANDOM_STATE,
        )

    def evaluate(self):

        X, y = self.benchmark.load_data()

        model = self.build_model()

        pipeline = self.benchmark.build_pipeline(
            model
        )

        cv = StratifiedKFold(
            n_splits=N_SPLITS,
            shuffle=True,
            random_state=RANDOM_STATE,
        )

        probabilities = cross_val_predict(
            pipeline,
            X,
            y,
            cv=cv,
            method="predict_proba",
            n_jobs=-1,
        )[:, 1]

        brier = brier_score_loss(
            y,
            probabilities,
        )

        fraction_positive, mean_predicted = calibration_curve(
            y,
            probabilities,
            n_bins=10,
            strategy="uniform",
        )

        return {
            "brier_score": float(brier),
            "fraction_positive": fraction_positive.tolist(),
            "mean_predicted": mean_predicted.tolist(),
            "probabilities": probabilities,
        }

    def save_results(self, results):

        artifacts_dir = Path(
            "ml/models/artifacts"
        )

        artifacts_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output = {
            "brier_score": results["brier_score"],
            "fraction_positive": results[
                "fraction_positive"
            ],
            "mean_predicted": results[
                "mean_predicted"
            ],
        }

        path = (
            artifacts_dir
            / "calibration_metrics.json"
        )

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                output,
                file,
                indent=2,
            )

        return path

    def plot(self, results):

        fraction_positive = results[
            "fraction_positive"
        ]

        mean_predicted = results[
            "mean_predicted"
        ]

        plt.figure(figsize=(7, 7))

        plt.plot(
            [0, 1],
            [0, 1],
            linestyle="--",
            label="Perfect calibration",
        )

        plt.plot(
            mean_predicted,
            fraction_positive,
            marker="o",
            label="MedGuard model",
        )

        plt.xlabel(
            "Mean predicted probability"
        )

        plt.ylabel(
            "Observed positive fraction"
        )

        plt.title(
            "Cardiovascular Risk Calibration"
        )

        plt.legend()
        plt.grid(True)

        output_dir = Path(
            "ml/models/artifacts"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = (
            output_dir
            / "calibration_curve.png"
        )

        plt.tight_layout()
        plt.savefig(path)
        plt.close()

        return path


if __name__ == "__main__":

    calibration = ModelCalibration(
        dataset_path=(
            "datasets/raw/"
            "heart_cleveland_upload.csv"
        )
    )

    results = calibration.evaluate()

    print("\n")
    print("=" * 80)
    print("MODEL CALIBRATION")
    print("=" * 80)

    print(
        f"\nBrier Score: "
        f"{results['brier_score']:.4f}"
    )

    metrics_path = calibration.save_results(
        results
    )

    curve_path = calibration.plot(
        results
    )

    print("\nARTIFACTS:")
    print(f"Metrics: {metrics_path}")
    print(f"Curve:   {curve_path}")
