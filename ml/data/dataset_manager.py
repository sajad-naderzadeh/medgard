from pathlib import Path
import pandas as pd


class DatasetManager:
    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)

    def load(self) -> pd.DataFrame:
        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {self.dataset_path}"
            )

        if self.dataset_path.suffix.lower() != ".csv":
            raise ValueError("Only CSV datasets are currently supported")

        return pd.read_csv(self.dataset_path)

    def summary(self, df: pd.DataFrame) -> dict:
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "features": list(df.columns),
            "missing_values": int(df.isna().sum().sum()),
            "duplicates": int(df.duplicated().sum()),
        }
