from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    # These fields match your .env keys automatically (case-insensitive)
    app_env: str = "dev"
    claude_model: str = "claude-sonnet-4-20250514"
    port: int = 8000
    context_dir: Path = Path("data/context")
    prompts_dir: Path = REPO_ROOT / "prompts"
    database_url: str = "sqlite+aiosqlite:///./var/mindlore.db"
    claude_api_key: str

    # This config tells Pydantic exactly where to find your file
    # and to ignore extra variables like OPEN_AI_KEY if they exist
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    # Native BaseSettings handles the from_env logic internally
    return Settings()
