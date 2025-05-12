"""Mocks for testing."""
from typing import Dict, List

# Mock of subfeddits database
MOCK_SUBFEDDITS = {
    "Dummy Topic 2": [
        {"id": 1, "text": "I love this topic"},
        {"id": 2, "text": "I don't agree"},
        {"id": 3, "text": "Excellent content"}
    ]
}

# Mock of subfeddit service
class MockSubfedditService:
    def get_subfeddit_id_by_name(self, name: str) -> str:
        if name in MOCK_SUBFEDDITS:
            return "123"
        return None

    def get_comments_by_subfeddit_id(self, subfeddit_id: str) -> List[Dict]:
        return MOCK_SUBFEDDITS["Dummy Topic 2"]

    def filter_comments_by_date(self, comments: List[Dict], start_time: str, end_time: str) -> List[Dict]:
        return comments

    def sort_comments_by_polarity(self, comments: List[Dict]) -> List[Dict]:
        return sorted(comments, key=lambda x: x['score'], reverse=True)