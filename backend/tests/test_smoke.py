def test_smoke_health_endpoint(app_client):
    response = app_client.get("/health")

    assert response.status_code == 200
