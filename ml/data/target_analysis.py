import pandas as pd


class TargetAnalyzer:

    def __init__(self, target_column: str):
        self.target_column = target_column

    def analyze(self, df: pd.DataFrame) -> dict:
        if self.target_column not in df.columns:
            raise ValueError(
                f"Target '{self.target_column}' not found"
            )

        target = df[self.target_column]

        distribution = (
            target
            .value_counts(dropna=False)
            .sort_index()
            .to_dict()
        )

        percentages = (
            target
            .value_counts(
                normalize=True,
                dropna=False,
            )
            .sort_index()
            .mul(100)
            .round(2)
            .to_dict()
        )

        return {
            "target": self.target_column,
            "unique_values": int(
                target.nunique(dropna=True)
            ),
            "missing_values": int(
                target.isna().sum()
            ),
            "distribution": distribution,
            "percentages": percentages,
        }
