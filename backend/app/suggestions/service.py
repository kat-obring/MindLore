from typing import Protocol, List
from app.prompts.repository import PromptRepository

class LLMClient(Protocol):
    def generate(self, prompt: str) -> str:
        """Generate text from prompt."""
        ...

class FakeLLMClient:
    def generate(self, prompt: str) -> str:
        return ""

class SuggestionService:
    def __init__(self, prompt_repo: "PromptRepository", llm_client: LLMClient):
        self.prompt_repo = prompt_repo
        self.llm_client = llm_client

    def get_suggestions(self, topic: str) -> List[str]:
        """Get 3 suggestions for a topic."""
        return []
