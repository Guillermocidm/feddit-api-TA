from src.sentiment_analysis_models import SentimentAnalysisModel, TextBlobSentimentAnalysis

def get_sentiment_analysis_model() -> SentimentAnalysisModel:
    return TextBlobSentimentAnalysis()