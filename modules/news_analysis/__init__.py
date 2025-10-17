"""
BuddyAI NEXTGEN - News & Sentiment Analysis Module

Analyzes global news, economic events, and market sentiment to inform trading decisions.
"""

from .news_fetcher import NewsFetcher
from .sentiment_analyzer import SentimentAnalyzer
from .event_detector import EventDetector
from .impact_analyzer import ImpactAnalyzer

__all__ = [
    'NewsFetcher',
    'SentimentAnalyzer',
    'EventDetector',
    'ImpactAnalyzer'
]
