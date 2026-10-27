import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class ClinicalPreprocessor:

    NUMERIC_FEATURES = [
        "age",
        "trestbps",
        "chol",
        "thalach",
        "oldpeak",
    ]

    CATEGORICAL_FEATURES = [
        "sex",
        "cp",
        "fbs",
        "restecg",
        "exang",
        "slope",
        "ca",
        "thal",
    ]

    def build(self) -> ColumnTransformer:

        numeric_pipeline = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(
                        strategy="median"
                    ),
                ),
                (
                    "scaler",
                    StandardScaler(),
                ),
            ]
        )

        categorical_pipeline = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(
                        strategy="most_frequent"
                    ),
                ),
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
                (
                    "numeric",
                    numeric_pipeline,
                    self.NUMERIC_FEATURES,
                ),
                (
                    "categorical",
                    categorical_pipeline,
                    self.CATEGORICAL_FEATURES,
                ),
            ]
        )

    def validate_columns(
        self,
        df: pd.DataFrame,
    ) -> None:

        expected = set(
            self.NUMERIC_FEATURES
            + self.CATEGORICAL_FEATURES
        )

        missing = expected - set(df.columns)

        if missing:
            raise ValueError(
                f"Missing feature columns: {sorted(missing)}"
            )
