import pandas as pd


class DataCleaner:
    def __init__(self, drop_duplicates: bool = True):
        self.drop_duplicates = drop_duplicates

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()

        if self.drop_duplicates:
            result = result.drop_duplicates()

        result = result.replace(
            ["?", "NA", "N/A", "null", "None", ""],
            pd.NA,
        )

        numeric_columns = result.select_dtypes(
            include=["number"]
        ).columns

        for column in numeric_columns:
            result[column] = result[column].fillna(
                result[column].median()
            )

        return result.reset_index(drop=True)
