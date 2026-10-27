import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, StratifiedKFold

from ml.training.benchmark import ModelBenchmark


RANDOM_STATE = 42


class HyperparameterTuner:

    def __init__(self, dataset_path: str):
        self.benchmark = ModelBenchmark(
            dataset_path=dataset_path
        )

    def tune_logistic_regression(self):

        X, y = self.benchmark.load_data()

        model = LogisticRegression(
            max_iter=3000,
            random_state=RANDOM_STATE,
        )

        pipeline = self.benchmark.build_pipeline(model)

        param_grid = {
            "model__C": [
                0.001,
                0.01,
                0.1,
                1.0,
                10.0,
                100.0,
            ],
            "model__solver": [
                "liblinear",
                "lbfgs",
            ],
            "model__class_weight": [
                None,
                "balanced",
            ],
        }

        cv = StratifiedKFold(
            n_splits=5,
            shuffle=True,
            random_state=RANDOM_STATE,
        )

        search = GridSearchCV(
            estimator=pipeline,
            param_grid=param_grid,
            scoring="roc_auc",
            cv=cv,
            n_jobs=-1,
            verbose=1,
            return_train_score=True,
        )

        search.fit(X, y)

        return search


if __name__ == "__main__":

    tuner = HyperparameterTuner(
        "datasets/raw/heart_cleveland_upload.csv"
    )

    search = tuner.tune_logistic_regression()

    print("\n")
    print("=" * 80)
    print("LOGISTIC REGRESSION HYPERPARAMETER TUNING")
    print("=" * 80)

    print("\nBEST PARAMETERS:")
    print(search.best_params_)

    print("\nBEST CV ROC-AUC:")
    print(f"{search.best_score_:.4f}")

    print("\nTOP CONFIGURATIONS:")

    results = pd.DataFrame(search.cv_results_)

    results = results[
        [
            "mean_test_score",
            "std_test_score",
            "mean_train_score",
            "params",
        ]
    ].sort_values(
        by="mean_test_score",
        ascending=False,
    )

    print(
        results.head(10).to_string(
            index=False
        )
    )
