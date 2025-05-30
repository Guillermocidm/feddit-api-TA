from transformers import pipeline
from .base import SentimentAnalysisModel


class TransformersSentimentAnalysis(SentimentAnalysisModel):
    """Sentiment analysis using the transformers pipeline."""

    def __init__(self) -> None:
        """Initialize the transformers sentiment analysis pipeline."""
        self.sentiment_pipeline = pipeline("sentiment-analysis")

    def classify(self, text: str) -> str:
        """
        Classify the sentiment of the text using transformers.

        :param text: The text to analyze.
        :return: A polarity score between -1.0 (negative) and 1.0 (positive).
        """
        result = self.sentiment_pipeline(text)
        if result[0]['label'] == "POSITIVE":
            return result[0]['score']
        else:
            return -result[0]['score']
