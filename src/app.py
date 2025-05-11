"""Main FastAPI application module."""
from fastapi import FastAPI, HTTPException, Depends
from typing import List, Dict, Any, Optional
from src.services.subfeddit_service import SubfedditService
from src.dependencies import get_sentiment_analysis_model

app = FastAPI()
subfeddit_service = SubfedditService()

@app.get('/subfeddit/analyze-comments/')
async def get_subfeddit_comments(
    name: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    sort_by_polarity: bool = False,
    sentiment_analysis_model = Depends(get_sentiment_analysis_model)
) -> List[Dict[str, Any]]:
    """
    Gets and analyzes comments from a specific subfeddit.
    
    Args:
        name (Optional[str]): Subfeddit name
        start_time (Optional[str]): Start date for filtering comments
        end_time (Optional[str]): End date for filtering comments
        sort_by_polarity (bool): Whether to sort comments by polarity
        sentiment_analysis_model: Dependency injected sentiment analysis model
        
    Returns:
        List[Dict[str, Any]]: List of analyzed comments
        
    Raises:
        HTTPException: If there are request or processing errors
    """
    if not name:
        raise HTTPException(status_code=400, detail="Subfeddit name is required")

    subfeddit_id = subfeddit_service.get_subfeddit_id_by_name(name)
    if not subfeddit_id:
        raise HTTPException(status_code=404, detail=f"{name} subfeddit not found")

    comments = subfeddit_service.get_comments_by_subfeddit_id(subfeddit_id)
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found")

    if start_time and end_time:
        comments = subfeddit_service.filter_comments_by_date(comments, start_time, end_time)

    scored_comments = [
        {
            'id': comment['id'],
            'text': comment['text'],
            'score': sentiment_analysis_model.classify(comment['text']),
            'category': "positive" if sentiment_analysis_model.classify(comment['text']) >= 0 else "negative"
        }
        for comment in comments
    ]

    if sort_by_polarity:
        scored_comments = subfeddit_service.sort_comments_by_polarity(scored_comments)

    return scored_comments

