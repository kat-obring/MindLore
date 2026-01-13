from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # These fields match your .env keys automatically (case-insensitive)
    app_env: str = "dev"
    openai_model: str = "gpt-5.2"
    port: int = 8000
    openai_api_key: str

    # This config tells Pydantic exactly where to find your file
    # and to ignore extra variables like OPEN_AI_KEY if they exist
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    # Native BaseSettings handles the from_env logic internally
    return Settings()