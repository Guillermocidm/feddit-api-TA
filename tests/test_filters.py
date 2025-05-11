import pytest
from src.services import SubfedditService as sf_service

@pytest.fixture
def mock_get_comments():
    """
    Fixture that returns a list of mock comments.
    """
    return [
        {'id': 1, 'text': 'This is awesome!', 'created_at': 1726704000, 'score': 1.0},   # 2024-09-19
        {'id': 2, 'text': 'This is bad...', 'created_at': 1726963200, 'score': -1.0},    # 2024-09-22
        {'id': 3, 'text': 'Neutral comment.', 'created_at': 1726617600, 'score': 0.0}    # 2024-09-18
    ]

def test_sort_by_polarity(mock_get_comments):
    """
    Test that comments are sorted correctly by polarity.
    """
    sorted_comments = sf_service.sort_comments_by_polarity(mock_get_comments)
    assert sorted_comments[0]['score'] == 1.0
    assert sorted_comments[1]['score'] == 0.0
    assert sorted_comments[2]['score'] == -1.0

def test_filter_by_date(mock_get_comments):
    """
    Test that filtering by date works correctly.
    """
    filtered_comments = sf_service.filter_comments_by_date(
        mock_get_comments, "2024-09-20", "2024-09-23"
    )
    assert len(filtered_comments) == 1
    assert filtered_comments[0]['text'] == 'This is bad...'