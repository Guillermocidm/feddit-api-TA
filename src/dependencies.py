from src.sentiment_analysis_models import SentimentAnalysisModel, TextBlobSentimentAnalysis
from src.services.subfeddit_service import SubfedditService

def get_sentiment_analysis_model() -> SentimentAnalysisModel:
    return TextBlobSentimentAnalysis()

def get_subfeddit_service() -> SubfedditService:
    return SubfedditService()