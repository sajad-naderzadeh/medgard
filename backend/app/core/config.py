from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "MedGuard AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "medguard"

    JWT_SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()


def validate_production_settings() -> None:
    """Fail closed when an unsafe development secret reaches production."""
    if (
        settings.ENVIRONMENT.lower() == "production"
        and settings.JWT_SECRET_KEY == "CHANGE_THIS_IN_PRODUCTION"
    ):
        raise RuntimeError(
            "JWT_SECRET_KEY must be set to a strong secret in production"
        )
