from unittest.mock import MagicMock

from backend.app.api.dependencies import get_suggestion_service
from fastapi.testclient import TestClient


def test_create_suggestions_returns_200_and_list_of_suggestions(app_client: TestClient):
    # Given a mocked suggestion service
    mock_service = MagicMock()
    mock_service.get_suggestions.return_value = [
        "### Outline A: Angle 1",
        "### Outline B: Angle 2",
        "### Outline C: Angle 3",
    ]
    app_client.app.dependency_overrides[get_suggestion_service] = lambda: mock_service

    # When
    response = app_client.post("/api/suggestions", json={"topic": "TDD for AI"})

    # Then
    if response.status_code != 200:
        print(response.json())
    assert response.status_code == 200
    payload = response.json()
    assert "suggestions" in payload
    assert len(payload["suggestions"]) == 3
    assert payload["suggestions"][0] == "### Outline A: Angle 1"

    # Cleanup
    app_client.app.dependency_overrides.clear()


def test_create_suggestions_with_empty_topic_returns_422(app_client: TestClient):
    # When
    response = app_client.post("/api/suggestions", json={"topic": "  "})

    # Then
    # We expect Pydantic to catch empty/whitespace strings if we use Field(min_length=1)
    assert response.status_code == 422
