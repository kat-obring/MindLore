import os
from ..prompts.repository import FilePromptRepository
from ..suggestions.service import SuggestionService, FakeLLMClient

def get_prompt_repository() -> FilePromptRepository:
    # Default to prompts directory relative to project root
    prompts_dir = os.getenv("PROMPTS_DIR", "../prompts")
    return FilePromptRepository(prompts_dir=prompts_dir)

def get_llm_client() -> FakeLLMClient:
    return FakeLLMClient()

def get_suggestion_service() -> SuggestionService:
    return SuggestionService(get_prompt_repository(), get_llm_client())
