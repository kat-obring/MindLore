from pathlib import Path
from typing import Protocol

TOPIC_SEPARATOR = "\n\nTopic:\n"


class PromptRepository(Protocol):
    def get_prompt(self, name: str) -> str:
        """Load prompt text by name."""
        ...


class FilePromptRepository:
    def __init__(self, prompts_dir: str):
        self.prompts_dir = Path(prompts_dir)

    def get_prompt(self, name: str) -> str:
        file_path = self.prompts_dir / f"{name}.md"
        return file_path.read_text(encoding="utf-8")


def render_prompt(prompt_template: str, topic: str) -> str:
    """Combine the prompt template with the topic."""
    return f"{prompt_template}{TOPIC_SEPARATOR}{topic}\n"
