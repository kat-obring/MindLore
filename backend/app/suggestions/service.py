import re
from typing import Protocol, List
from app.prompts.repository import PromptRepository, render_prompt

class LLMClient(Protocol):
    def generate(self, prompt: str) -> str:
        """Generate text from prompt."""
        ...

class FakeLLMClient:
    def __init__(self):
        self.last_prompt = None

    def generate(self, prompt: str) -> str:
        self.last_prompt = prompt
        return ""

class OpenAIClient:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str) -> str:
        import httpx
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        with httpx.Client() as client:
            response = client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=60.0
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"] or ""

class SuggestionService:
    def __init__(self, prompt_repo: PromptRepository, llm_client: LLMClient):
        self.prompt_repo = prompt_repo
        self.llm_client = llm_client

    def get_suggestions(self, topic: str) -> List[str]:
        """Get 3 suggestions for a topic."""
        prompt_template = self.prompt_repo.get_prompt("topics_first")
        final_prompt = render_prompt(prompt_template, topic)
        response = self.llm_client.generate(final_prompt)
        return parse_suggestions(response)

def parse_suggestions(text: str) -> List[str]:
    """Parse the LLM response into exactly 3 suggestions."""
    # Pattern to find all markers (using lookahead to keep the marker in the split result)
    pattern = r"(?=### Outline [ABC]:)"
    parts = re.split(pattern, text)
    
    # Filter for parts that start with our marker and strip whitespace
    suggestions = [p.strip() for p in parts if p.strip().startswith("### Outline")]
    
    if len(suggestions) != 3:
        raise ValueError(f"Expected exactly 3 suggestions, found {len(suggestions)}")
        
    return suggestions
