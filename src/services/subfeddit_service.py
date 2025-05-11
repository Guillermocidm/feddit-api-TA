"""Service layer for subfeddit-related operations."""
from typing import List, Optional, Dict, Any
import requests
from datetime import datetime
from src.constants import (
    SUBFEDDITS_URL,
    COMMENTS_URL,
    DEFAULT_SUBFEDDIT_LIMIT,
    DEFAULT_COMMENTS_LIMIT,
    DEFAULT_SKIP,
    DATE_FORMAT
)

class SubfedditService:
    """Service class for handling subfeddit operations."""

    @staticmethod
    def get_subfeddit_id_by_name(name: str) -> Optional[int]:
        """
        Gets a subfeddit ID by its name.
        
        Args:
            name (str): Name of the subfeddit to search for
            
        Returns:
            Optional[int]: Subfeddit ID if found, None otherwise
        """
        skip = DEFAULT_SKIP
        while True:
            try:
                parameters = f"?skip={skip}&limit={DEFAULT_SUBFEDDIT_LIMIT}"
                response = requests.get(SUBFEDDITS_URL + parameters)
                response.raise_for_status()
            except requests.exceptions.RequestException as error:
                print(f"Error {error}")
                return None
                
            subfeddits = response.json().get("subfeddits")
            for subfeddit in subfeddits:
                if subfeddit['title'] == name:
                    return subfeddit['id']
                    
            if len(subfeddits) < DEFAULT_SUBFEDDIT_LIMIT:
                break
            skip += DEFAULT_SUBFEDDIT_LIMIT
        return None

    @staticmethod
    def get_comments_by_subfeddit_id(
        id: int, 
        skip: int = DEFAULT_SKIP, 
        limit: int = DEFAULT_COMMENTS_LIMIT
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Gets comments from a specific subfeddit.
        
        Args:
            id (int): Subfeddit ID
            skip (int, optional): Number of comments to skip
            limit (int, optional): Maximum number of comments to retrieve
            
        Returns:
            Optional[List[Dict[str, Any]]]: List of comments if found, None otherwise
        """
        parameters = f"?subfeddit_id={id}&skip={skip}&limit={limit}"
        try:
            response = requests.get(COMMENTS_URL + parameters)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(f"Error {error}")
            return None
        return response.json().get('comments')

    @staticmethod
    def filter_comments_by_date(
        comments: List[Dict[str, Any]], 
        start_time: Optional[str] = None, 
        end_time: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Filters comments by date range.
        
        Args:
            comments (List[Dict[str, Any]]): List of comments to filter
            start_time (Optional[str]): Start date in 'YYYY-MM-DD' format
            end_time (Optional[str]): End date in 'YYYY-MM-DD' format
            
        Returns:
            List[Dict[str, Any]]: Filtered list of comments
        """
        filtered_comments = []
        for comment in comments:
            comment_time = datetime.fromtimestamp(comment['created_at'])
            
            if start_time:
                start_time_dt = datetime.strptime(start_time, DATE_FORMAT)
                if comment_time < start_time_dt:
                    continue
                    
            if end_time:
                end_time_dt = datetime.strptime(end_time, DATE_FORMAT)
                if comment_time > end_time_dt:
                    continue
                    
            filtered_comments.append(comment)
        return filtered_comments

    @staticmethod
    def sort_comments_by_polarity(scored_comments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Sorts comments by polarity score.
        
        Args:
            scored_comments (List[Dict[str, Any]]): List of comments with scores
            
        Returns:
            List[Dict[str, Any]]: List of comments sorted by polarity
        """
        return sorted(scored_comments, key=lambda x: x['score'], reverse=True) 