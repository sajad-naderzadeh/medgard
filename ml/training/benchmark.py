from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
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
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from xgboost import XGBClassifier

from ml.preprocessing.pipeline import ClinicalPreprocessor
from ml.preprocessing.clinical_features import ClinicalFeatureEngineer


RANDOM_STATE = 42


class ModelBenchmark:
    """Train and benchmark baseline cardiovascular risk models."""

    def __init__(self, dataset_path: str, target_column: str = "condition"):
        self.dataset_path = Path(dataset_path)
        self.target_column = target_column

    def load_data(self):
        df = pd.read_csv(self.dataset_path)

        X = df.drop(columns=[self.target_column])
        y = df[self.target_column]

        feature_engineer = ClinicalFeatureEngineer()
        X = feature_engineer.transform(X)

        return X, y

    def build_preprocessor(self):
        numeric_features = [
            "age",
            "trestbps",
            "chol",
            "thalach",
            "oldpeak",
            "age_max_hr_ratio",
            "bp_age_interaction",
            "chol_age_ratio",
        ]

        categorical_features = [
            "sex",
            "cp",
            "fbs",
            "restecg",
            "exang",
            "slope",
            "ca",
            "thal",
        ]

        numeric_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )

        categorical_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                (
                    "onehot",
                    OneHotEncoder(
                        handle_unknown="ignore",
                        sparse_output=False,
                    ),
                ),
            ]
        )

        return ColumnTransformer(
            transformers=[
                ("numeric", numeric_pipeline, numeric_features),
                ("categorical", categorical_pipeline, categorical_features),
            ]
        )

    def build_models(self):
        return {
            "logistic_regression": LogisticRegression(
                max_iter=2000,
                random_state=RANDOM_STATE,
            ),
            "random_forest": RandomForestClassifier(
                n_estimators=300,
                max_depth=None,
                min_samples_split=2,
                random_state=RANDOM_STATE,
                n_jobs=-1,
            ),
            "xgboost": XGBClassifier(
                n_estimators=300,
                max_depth=4,
                learning_rate=0.05,
                subsample=0.9,
                colsample_bytree=0.9,
                objective="binary:logistic",
                eval_metric="logloss",
                random_state=RANDOM_STATE,
                n_jobs=-1,
            ),
        }

    @staticmethod
    def calculate_metrics(y_true, y_probability, threshold=0.5):
        y_pred = (y_probability >= threshold).astype(int)

        tn, fp, fn, tp = confusion_matrix(
            y_true,
            y_pred,
            labels=[0, 1],
        ).ravel()

        specificity = tn / (tn + fp) if (tn + fp) else 0.0

        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "roc_auc": roc_auc_score(y_true, y_probability),
            "pr_auc": average_precision_score(y_true, y_probability),
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

    def build_pipeline(self, model):
        return Pipeline(
            steps=[
                ("preprocessor", self.build_preprocessor()),
                ("model", clone(model)),
            ]
        )

    def train(self):
        X, y = self.load_data()
        models = self.build_models()

        results = []
        trained_models = {}

        for model_name, model in models.items():
            pipeline = self.build_pipeline(model)

            pipeline.fit(X, y)

            probabilities = pipeline.predict_proba(X)[:, 1]

            metrics = self.calculate_metrics(
                y_true=y,
                y_probability=probabilities,
            )

            metrics["model"] = model_name

            results.append(metrics)
            trained_models[model_name] = pipeline

        results_df = pd.DataFrame(results)

        results_df = results_df[
            [
                "model",
                "roc_auc",
                "pr_auc",
                "accuracy",
                "precision",
                "recall",
                "specificity",
                "f1",
            ]
        ]

        return results_df, trained_models


if __name__ == "__main__":
    benchmark = ModelBenchmark(
        dataset_path="datasets/raw/heart_cleveland_upload.csv"
    )

    results, models = benchmark.train()

    print("\nMODEL BENCHMARK")
    print("=" * 80)
    print(results.to_string(index=False))
