import pandas as pd

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


class CrossValidator:
    def __init__(
        self,
        dataset_path: str,
        target_column: str = "condition",
    ):
        self.benchmark = ModelBenchmark(
            dataset_path=dataset_path,
            target_column=target_column,
        )

    @staticmethod
    def calculate_metrics(y_true, y_probability):
        y_pred = (y_probability >= 0.5).astype(int)

        tn, fp, fn, tp = confusion_matrix(
            y_true,
            y_pred,
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
                y_probability,
            ),
            "pr_auc": average_precision_score(
                y_true,
                y_probability,
            ),
            "accuracy": accuracy_score(
                y_true,
                y_pred,
            ),
            "precision": precision_score(
                y_true,
                y_pred,
                zero_division=0,
            ),
            "recall": recall_score(
                y_true,
                y_pred,
                zero_division=0,
            ),
            "specificity": specificity,
            "f1": f1_score(
                y_true,
                y_pred,
                zero_division=0,
            ),
        }

    def run(self):
        X, y = self.benchmark.load_data()

        models = self.benchmark.build_models()

        cv = StratifiedKFold(
            n_splits=N_SPLITS,
            shuffle=True,
            random_state=RANDOM_STATE,
        )

        all_results = []

        for model_name, model in models.items():

            fold_metrics = []

            print(f"\nEvaluating: {model_name}")

            for fold, (train_idx, test_idx) in enumerate(
                cv.split(X, y),
                start=1,
            ):
                X_train = X.iloc[train_idx]
                X_test = X.iloc[test_idx]

                y_train = y.iloc[train_idx]
                y_test = y.iloc[test_idx]

                pipeline = self.benchmark.build_pipeline(model)

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

                fold_metrics.append(metrics)

                print(
                    f"  Fold {fold}: "
                    f"ROC-AUC={metrics['roc_auc']:.4f} "
                    f"F1={metrics['f1']:.4f}"
                )

            fold_df = pd.DataFrame(fold_metrics)

            summary = {
                "model": model_name,
            }

            metrics_to_summarize = [
                "roc_auc",
                "pr_auc",
                "accuracy",
                "precision",
                "recall",
                "specificity",
                "f1",
            ]

            for metric in metrics_to_summarize:
                summary[f"{metric}_mean"] = (
                    fold_df[metric].mean()
                )

                summary[f"{metric}_std"] = (
                    fold_df[metric].std()
                )

            all_results.append(summary)

        return pd.DataFrame(all_results)


if __name__ == "__main__":

    validator = CrossValidator(
        dataset_path="datasets/raw/heart_cleveland_upload.csv"
    )

    results = validator.run()

    print("\n")
    print("=" * 110)
    print("5-FOLD STRATIFIED CROSS-VALIDATION")
    print("=" * 110)

    print(
        results.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )
