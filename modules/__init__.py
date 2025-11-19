"""
NFL News & Odds Aggregator - Modules Package
Modular components for the Streamlit application
"""

from .config_manager import ConfigManager
from .news_fetcher import RSSFeedFetcher, NewsDataProcessor, fetch_all_news_articles
from .odds_fetcher import OddsFetcher
from .theme_manager import ThemeManager
from .ui_components import UIComponents

__all__ = [
    'ConfigManager',
    'RSSFeedFetcher',
    'NewsDataProcessor',
    'fetch_all_news_articles',
    'OddsFetcher',
    'ThemeManager',
    'UIComponents'
]

__version__ = '1.0.0'
__author__ = 'Your Name'
__description__ = 'NFL News & Odds Aggregator with modular architecture'
