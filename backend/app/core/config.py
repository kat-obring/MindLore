import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel


class Settings(BaseModel):
    app_env: str = "dev"
    openai_model: str = "gpt-5.2"
    port: int = 8000
    openai_api_key: str

    def __init__(self, **data):
        if not data:
            data = self._load_env()
        super().__init__(**data)

    @classmethod
    def _load_env(cls) -> dict:
        values = {
            "app_env": os.getenv("APP_ENV", cls.model_fields["app_env"].default),
            "openai_model": os.getenv(
                "OPENAI_MODEL", cls.model_fields["openai_model"].default
            ),
            "port": os.getenv("PORT", cls.model_fields["port"].default),
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
        }

        return values


@lru_cache
def get_settings() -> Settings:
    load_dotenv()
    return Settings()
