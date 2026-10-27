import pandas as pd


class ClinicalFeatureEngineer:

    def transform(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        result = df.copy()

        if {
            "age",
            "thalach",
        }.issubset(result.columns):

            max_hr = 220 - result["age"]

            result["age_max_hr_ratio"] = (
                result["thalach"] / max_hr
            )

        if {
            "trestbps",
            "age",
        }.issubset(result.columns):

            result["bp_age_interaction"] = (
                result["trestbps"]
                * result["age"]
            )

        if {
            "chol",
            "age",
        }.issubset(result.columns):

            result["chol_age_ratio"] = (
                result["chol"]
                / result["age"]
            )

        return result
