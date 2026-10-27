import pandas as pd


class FeatureEngineer:
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()

        if {"weight", "height"}.issubset(result.columns):
            height_m = result["height"] / 100
            result["bmi"] = result["weight"] / (height_m ** 2)

        if {"systolic_bp", "diastolic_bp"}.issubset(result.columns):
            result["pulse_pressure"] = (
                result["systolic_bp"]
                - result["diastolic_bp"]
            )

        return result
