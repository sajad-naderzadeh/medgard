import pytest

from app.core.config import settings, validate_production_settings


def test_production_rejects_default_jwt_secret(monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    monkeypatch.setattr(settings, "JWT_SECRET_KEY", "CHANGE_THIS_IN_PRODUCTION")

    with pytest.raises(RuntimeError, match="JWT_SECRET_KEY"):
        validate_production_settings()
