import pytest
import requests

# Base URL for API tests
BASE_URL = "http://localhost:5000/subfeddit/analyze-comments/"

def test_get_comments():
    """
    Test that the API returns comments correctly for a valid subfeddit.
    """
    params = {'name': 'Dummy Topic 2'}
    response = requests.get(BASE_URL, params=params)
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
    Test that the API returns 404 if the subfeddit does not exist.
    """
    params = {'name': 'AAAA'}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 404
    assert response.json().get('detail') == f"{params['name']} subfeddit not found"

def test_subfeddit_name_required():
    """
    Test that the API returns 400 if the subfeddit name is not provided.
    """
    params = {'name': '', 'sort_by_polarity': 'true'}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 400
    assert response.json().get('detail') == "Subfeddit name is required"
