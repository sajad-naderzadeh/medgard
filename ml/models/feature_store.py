from pathlib import Path
import pandas as pd


class FeatureStore:
    def __init__(self, storage_path: str = "ml/data/features"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def save(self, df: pd.DataFrame, name: str) -> Path:
        path = self.storage_path / f"{name}.csv"
        df.to_csv(path, index=False)
        return path

    def load(self, name: str) -> pd.DataFrame:
        path = self.storage_path / f"{name}.csv"

        if not path.exists():
            raise FileNotFoundError(
                f"Feature dataset not found: {path}"
            )

        return pd.read_csv(path)
