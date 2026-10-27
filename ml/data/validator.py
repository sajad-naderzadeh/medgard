import pandas as pd


class DataValidator:
    def __init__(self, required_columns: list[str]):
        self.required_columns = required_columns

    def validate(self, df: pd.DataFrame) -> dict:
        missing_columns = [
            column
            for column in self.required_columns
            if column not in df.columns
        ]

        return {
            "valid": len(missing_columns) == 0,
            "missing_columns": missing_columns,
            "rows": len(df),
            "columns": len(df.columns),
        }

    def validate_target(
        self,
        df: pd.DataFrame,
        target_column: str,
    ) -> dict:
        if target_column not in df.columns:
            return {
                "valid": False,
                "error": f"Target column '{target_column}' not found",
            }

        return {
            "valid": True,
            "target_column": target_column,
            "unique_values": df[target_column].nunique(),
            "missing_values": int(df[target_column].isna().sum()),
        }
