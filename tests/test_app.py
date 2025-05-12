import pytest
from fastapi.testclient import TestClient
from src.app import app
from src.dependencies import get_subfeddit_service
from tests.mocks import MockSubfedditService

# Configure the test client
client = TestClient(app)

# Replace the real services with mocks
app.dependency_overrides[get_subfeddit_service] = lambda: MockSubfedditService()

def test_get_comments():
    """
    Test that verifies that the API returns comments correctly for a valid subfeddit.
    """
    response = client.get("/subfeddit/analyze-comments/", params={"name": "Dummy Topic 2"})
    data = response.json()

    assert response.status_code == 200
    assert len(data) > 0
    assert list(data[0].keys()) == ['id', 'text', 'score', 'category']
    for d in data:
        assert isinstance(d['score'], float)
        assert -1.0 <= d['score'] <= 1.0
        if d['score'] >= 0.0:
            assert d['category'] == 'positive'
        else:
            assert d['category'] == 'negative'

def test_subfeddit_not_found():
    """
    Test that verifies that the API returns 404 if the subfeddit does not exist.
    """
    response = client.get("/subfeddit/analyze-comments/", params={"name": "AAAA"})
    assert response.status_code == 404
    assert response.json().get('detail') == "AAAA subfeddit not found"

def test_subfeddit_name_required():
    """
    Test that verifies that the API returns 400 if the subfeddit name is not provided.
    """
    response = client.get("/subfeddit/analyze-comments/", params={"name": ""})
    assert response.status_code == 400
    assert response.json().get('detail') == "Subfeddit name is required"
