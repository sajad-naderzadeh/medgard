import mlflow


class MLflowTracker:
    def __init__(
        self,
        experiment_name: str = "medguard-cardiovascular-risk",
    ):
        mlflow.set_experiment(experiment_name)

    def start_run(self, run_name: str | None = None):
        return mlflow.start_run(run_name=run_name)

    @staticmethod
    def log_params(params: dict):
        mlflow.log_params(params)

    @staticmethod
    def log_metrics(metrics: dict):
        mlflow.log_metrics(metrics)

    @staticmethod
    def log_model(model, artifact_path: str = "model"):
        mlflow.sklearn.log_model(
            model,
            artifact_path,
        )
