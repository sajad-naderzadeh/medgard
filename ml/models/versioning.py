from datetime import datetime, timezone
from pathlib import Path
import shutil


class ModelVersioning:
    def __init__(self, registry_path: str = "ml/models/registry"):
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def register(
        self,
        model_path: str,
        version: str,
    ) -> Path:
        source = Path(model_path)

        if not source.exists():
            raise FileNotFoundError(
                f"Model not found: {source}"
            )

        version_dir = self.registry_path / version
        version_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = version_dir / "model.joblib"
        shutil.copy2(source, destination)

        metadata = version_dir / "metadata.txt"
        metadata.write_text(
            f"version={version}\n"
            f"registered_at="
            f"{datetime.now(timezone.utc).isoformat()}\n",
            encoding="utf-8",
        )

        return destination
