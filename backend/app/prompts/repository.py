from typing import Protocol

import os

class PromptRepository(Protocol):
    def get_prompt(self, name: str) -> str:
        """Load prompt text by name."""
        ...

class FilePromptRepository:
    def __init__(self, prompts_dir: str):
        self.prompts_dir = prompts_dir

    def get_prompt(self, name: str) -> str:
        file_path = os.path.join(self.prompts_dir, f"{name}.md")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
