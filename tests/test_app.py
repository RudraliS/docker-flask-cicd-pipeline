import pytest
from app.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that home page loads with 200 OK and contains expected title."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Dockerized Flask App" in response.data

def test_health_endpoint(client):
    """Test the /health endpoint returns status: healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data is not None
    assert json_data["status"] == "healthy"
    assert "version" in json_data
    assert "timestamp" in json_data

def test_api_info_endpoint(client):
    """Test the /api/info endpoint returns correct app metadata."""
    response = client.get("/api/info")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data is not None
    assert json_data["app_name"] == "Dockerized Flask CI/CD Demo"
    assert "runtime" in json_data
