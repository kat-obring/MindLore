import os
from typing import Union
from ..prompts.repository import FilePromptRepository
from ..suggestions.service import SuggestionService, FakeLLMClient, OpenAIClient, LLMClient
from ..core.config import get_settings

def get_prompt_repository() -> FilePromptRepository:
    # Default to prompts directory relative to project root
    prompts_dir = os.getenv("PROMPTS_DIR", "../prompts")
    return FilePromptRepository(prompts_dir=prompts_dir)

def get_llm_client() -> LLMClient:
    settings = get_settings()
    # In a real app, we might check APP_ENV or similar
    # For now, if we have a real key, we can use the real client
    # but for tests, we will use dependency_overrides.
    return OpenAIClient(api_key=settings.openai_api_key, model=settings.openai_model)

def get_suggestion_service() -> SuggestionService:
    return SuggestionService(get_prompt_repository(), get_llm_client())
