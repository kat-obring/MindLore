import pytest
from app.suggestions.service import SuggestionService, FakeLLMClient
from app.prompts.repository import render_prompt

class MockPromptRepo:
    def get_prompt(self, name: str) -> str:
        return f"Template for {name}"

def test_suggestion_service_calls_llm_with_rendered_prompt():
    # Given
    prompt_repo = MockPromptRepo()
    llm_client = FakeLLMClient()
    service = SuggestionService(prompt_repo=prompt_repo, llm_client=llm_client)
    topic = "Scaling Quality Engineering"
    
    # When
    service.get_suggestions(topic)
    
    # Then
    expected_prompt = render_prompt("Template for topics_first", topic)
    assert llm_client.last_prompt == expected_prompt
