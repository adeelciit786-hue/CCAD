"""
Champion Cleaners Google Ads Decision Support Bot
AI-powered analysis and recommendations for Google Ads campaigns.
"""

from .data_loader import DataLoader
from .analyzer import PerformanceAnalyzer
from .recommender import RecommendationEngine

__version__ = "1.0.0"
__author__ = "Champion Cleaners Analytics Team"

__all__ = [
    'DataLoader',
    'PerformanceAnalyzer',
    'RecommendationEngine'
]
