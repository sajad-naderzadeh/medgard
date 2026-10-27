import pandas as pd


class DatasetStatistics:

    @staticmethod
    def numeric_summary(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        return df.describe().transpose()

    @staticmethod
    def categorical_summary(
        df: pd.DataFrame,
    ) -> dict:
        result = {}

        for column in df.columns:
            if df[column].dtype == "object":
                result[column] = (
                    df[column]
                    .value_counts(
                        dropna=False
                    )
                    .to_dict()
                )

        return result

    @staticmethod
    def correlation_matrix(
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        return df.corr(numeric_only=True)
