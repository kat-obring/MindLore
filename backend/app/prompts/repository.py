from typing import Protocol

class PromptRepository(Protocol):
    def get_prompt(self, name: str) -> str:
        """Load prompt text by name."""
        ...

class FilePromptRepository:
    def get_prompt(self, name: str) -> str:
        return ""
