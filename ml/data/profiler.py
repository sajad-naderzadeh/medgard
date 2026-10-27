from pathlib import Path
import pandas as pd


class DatasetProfiler:
    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)

    def load(self) -> pd.DataFrame:
        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {self.dataset_path}"
            )

        return pd.read_csv(self.dataset_path)

    def profile(self, df: pd.DataFrame) -> dict:
        return {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": df.columns.tolist(),
            "dtypes": {
                column: str(dtype)
                for column, dtype in df.dtypes.items()
            },
            "missing_values": {
                column: int(count)
                for column, count in df.isna().sum().items()
            },
            "duplicates": int(df.duplicated().sum()),
            "numeric_columns": df.select_dtypes(
                include="number"
            ).columns.tolist(),
            "categorical_columns": df.select_dtypes(
                exclude="number"
            ).columns.tolist(),
        }
