import mlflow


class ModelRegistry:
    def __init__(
        self,
        model_name: str = "MedGuard-CVD-Risk",
    ):
        self.model_name = model_name

    def register_from_run(
        self,
        run_id: str,
        artifact_path: str = "model",
    ):
        model_uri = f"runs:/{run_id}/{artifact_path}"

        return mlflow.register_model(
            model_uri=model_uri,
            name=self.model_name,
        )
