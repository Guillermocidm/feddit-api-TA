"""Constants used across the application."""

# API URLs
FEDDIT_BASE_URL = "http://feddit:8080/api/v1"
SUBFEDDITS_URL = f"{FEDDIT_BASE_URL}/subfeddits/"
COMMENTS_URL = f"{FEDDIT_BASE_URL}/comments/"

# Pagination defaults
DEFAULT_SUBFEDDIT_LIMIT = 10
DEFAULT_COMMENTS_LIMIT = 50
DEFAULT_SKIP = 0

# Date format
DATE_FORMAT = '%Y-%m-%d' 