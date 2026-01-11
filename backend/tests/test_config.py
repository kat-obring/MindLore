import pytest
from pydantic import ValidationError

from backend.app.core.config import Settings


def _clear_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("APP_ENV", "OPENAI_MODEL", "PORT", "OPENAI_API_KEY"):
        monkeypatch.delenv(key, raising=False)


def test_settings_load_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_env(monkeypatch)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-default-123")

    settings = Settings()

    assert settings.app_env == "dev"
    assert settings.openai_model == "gpt-5.2"
    assert settings.port == 8000


def test_settings_apply_env_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_env(monkeypatch)
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4.1")
    monkeypatch.setenv("PORT", "9001")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-123")

    settings = Settings()

    assert settings.app_env == "test"
    assert settings.openai_model == "gpt-4.1"
    assert settings.port == 9001
    assert settings.openai_api_key == "sk-test-123"


def test_settings_require_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_env(monkeypatch)

    with pytest.raises(ValidationError):
        Settings()

    monkeypatch.setenv("OPENAI_API_KEY", "sk-required-123")

    settings = Settings()

    assert settings.openai_api_key == "sk-required-123"
