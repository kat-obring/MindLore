from unittest.mock import MagicMock

from backend.app.prompts.repository import render_prompt
from backend.app.suggestions.service import FakeLLMClient, SuggestionService


class MockPromptRepo:
    def get_prompt(self, name: str) -> str:
        return f"Template for {name}"


def test_suggestion_service_calls_llm_with_rendered_prompt():
    # Given
    prompt_repo = MockPromptRepo()
    llm_client = FakeLLMClient()

    # Mock the return value to avoid parsing error
    mock_response = "### Outline A: 1\n### Outline B: 2\n### Outline C: 3"

    # We use a side effect to capture the prompt AND return the mock response
    def mock_generate(prompt):
        llm_client.last_prompt = prompt
        return mock_response

    llm_client.generate = MagicMock(side_effect=mock_generate)

    service = SuggestionService(prompt_repo=prompt_repo, llm_client=llm_client)
    topic = "Scaling Quality Engineering"

    # When
    service.get_suggestions(topic)

    # Then
    expected_prompt = render_prompt("Template for topics_first", topic)
    assert llm_client.last_prompt == expected_prompt
