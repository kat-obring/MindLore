from fastapi.testclient import TestClient


def test_health_endpoint_returns_status_env_version(app_client: TestClient) -> None:
    response = app_client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["env"] == app_client.app.state.settings.app_env
    assert payload["version"] == app_client.app.state.version
