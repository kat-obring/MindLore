from unittest.mock import MagicMock, patch

from backend.app.suggestions.service import OpenAIClient


def test_openai_client_calls_api_correctly():
    # Given
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Suggestions from OpenAI"}}]
    }
    mock_response.status_code = 200

    with patch("httpx.Client") as mock_client_class:
        mock_client = mock_client_class.return_value.__enter__.return_value
        mock_client.post.return_value = mock_response

        client = OpenAIClient(api_key="fake-key", model="gpt-5.2")

        # When
        result = client.generate("Test prompt")

        # Then
        assert result == "Suggestions from OpenAI"
        mock_client.post.assert_called_once()
        _, kwargs = mock_client.post.call_args
        assert kwargs["json"]["model"] == "gpt-5.2"
        assert kwargs["json"]["messages"][0]["content"] == "Test prompt"
        assert kwargs["headers"]["Authorization"] == "Bearer fake-key"
