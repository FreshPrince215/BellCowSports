"""
News Fetcher Module
Handles RSS feed fetching and processing for NFL news
"""

import feedparser
import pandas as pd
import hashlib
import re
import time
import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from email.utils import parsedate_to_datetime
import pytz

class RSSFeedFetcher:
    """Handles RSS feed fetching with robust error handling and parallel processing"""
    
    def __init__(self, days_lookback: int = 7, max_entries: int = 100):
        self.days_lookback = days_lookback
        self.max_entries = max_entries
        self.cutoff_date = datetime.now() - timedelta(days=days_lookback)
        self.successful_fetches = 0
        self.failed_fetches = 0
    
    def sanitize_html_content(self, text: str) -> str:
        """Remove HTML tags and clean text content"""
        if not text:
            return ""
        text = re.sub(r'<[^>]+>', '', text)
        text = ' '.join(text.split())
        if len(text) > 300:
            text = text[:300] + '...'
        return text
    
    def fetch_feed(self, url: str, source_name: str = "") -> List[Dict]:
        """Fetch a single RSS feed with comprehensive error handling"""
        try:
            feed = feedparser.parse(url, request_headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if not feed.entries:
                self.failed_fetches += 1
                return []
            
            # Define EST timezone
            est = pytz.timezone('US/Eastern')
            utc = pytz.UTC
            
            articles = []
            for entry in feed.entries[:self.max_entries]:
                title = entry.get('title', '').strip()
                link = entry.get('link', '')
                
                if not title or not link:
                    continue
                
                # IMPROVED DATE PARSING WITH EST CONVERSION
                pub_date = None
                
                # Try published_parsed first, then updated_parsed
                pub_parsed = entry.get('published_parsed') or entry.get('updated_parsed')
                
                if pub_parsed:
                    try:
                        # Convert struct_time to UTC datetime
                        pub_date = datetime.fromtimestamp(time.mktime(pub_parsed), tz=utc)
                    except (ValueError, OverflowError, OSError):
                        pass
                
                # If parsing failed or no date found, try string parsing
                if pub_date is None:
                    for date_field in ['published', 'updated']:
                        date_str = entry.get(date_field, '')
                        if date_str:
                            try:
                                pub_date = parsedate_to_datetime(date_str)
                                # If timezone-naive, assume UTC
                                if pub_date.tzinfo is None:
                                    pub_date = utc.localize(pub_date)
                                break
                            except:
                                pass
                
                # Fall back to current time in UTC if all parsing failed
                if pub_date is None:
                    pub_date = datetime.now(utc)
                
                # Convert to EST
                pub_date_est = pub_date.astimezone(est)
                
                # Make timezone-naive for storage and comparison
                pub_date_naive = pub_date_est.replace(tzinfo=None)
                
                if pub_date_naive >= self.cutoff_date:
                    summary = entry.get('summary', entry.get('description', ''))
                    summary = self.sanitize_html_content(summary)
                    
                    articles.append({
                        'title': title,
                        'link': link,
                        'published': pub_date_naive,
                        'source': source_name,
                        'summary': summary
                    })
            
            self.successful_fetches += 1
            return articles
            
        except Exception as e:
            self.failed_fetches += 1
            return []
    
    def fetch_multiple_feeds(self, feeds: List[Tuple[str, str]], max_workers: int = 10) -> List[Dict]:
        """Fetch multiple RSS feeds in parallel for improved performance"""
        articles = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.fetch_feed, url, name): (url, name)
                      for url, name in feeds}
            
            for future in as_completed(futures):
                try:
                    articles.extend(future.result())
                except:
                    pass
        
        return articles


class NewsDataProcessor:
    """Utilities for processing and cleaning news data"""
    
    @staticmethod
    def generate_content_hash(text: str) -> str:
        """Generate MD5 hash for content deduplication"""
        return hashlib.md5(text.encode()).hexdigest()
    
    @staticmethod
    def remove_duplicate_articles(df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate articles based on headline content"""
        if df.empty:
            return df
        
        df['content_hash'] = df['headline'].apply(NewsDataProcessor.generate_content_hash)
        df = df.drop_duplicates(subset=['content_hash']).drop(columns=['content_hash'])
        
        return df
    
    @staticmethod
    def identify_team_from_content(text: str, teams: List[str]) -> str:
        """Extract NFL team name from article content using keyword matching"""
        text_upper = text.upper()
        
        team_keyword_mapping = {
            'CARDINALS': 'Arizona Cardinals',
            'FALCONS': 'Atlanta Falcons',
            'RAVENS': 'Baltimore Ravens',
            'BILLS': 'Buffalo Bills',
            'PANTHERS': 'Carolina Panthers',
            'BEARS': 'Chicago Bears',
            'BENGALS': 'Cincinnati Bengals',
            'BROWNS': 'Cleveland Browns',
            'COWBOYS': 'Dallas Cowboys',
            'BRONCOS': 'Denver Broncos',
            'LIONS': 'Detroit Lions',
            'PACKERS': 'Green Bay Packers',
            'TEXANS': 'Houston Texans',
            'COLTS': 'Indianapolis Colts',
            'JAGUARS': 'Jacksonville Jaguars',
            'CHIEFS': 'Kansas City Chiefs',
            'RAIDERS': 'Las Vegas Raiders',
            'CHARGERS': 'Los Angeles Chargers',
            'RAMS': 'Los Angeles Rams',
            'DOLPHINS': 'Miami Dolphins',
            'VIKINGS': 'Minnesota Vikings',
            'PATRIOTS': 'New England Patriots',
            'SAINTS': 'New Orleans Saints',
            'GIANTS': 'New York Giants',
            'JETS': 'New York Jets',
            'EAGLES': 'Philadelphia Eagles',
            'STEELERS': 'Pittsburgh Steelers',
            '49ERS': 'San Francisco 49ers',
            'SEAHAWKS': 'Seattle Seahawks',
            'BUCCANEERS': 'Tampa Bay Buccaneers',
            'BUCS': 'Tampa Bay Buccaneers',
            'TITANS': 'Tennessee Titans',
            'COMMANDERS': 'Washington Commanders'
        }
        
        for keyword, team in team_keyword_mapping.items():
            if keyword in text_upper:
                return team
        
        for team in teams:
            if team.upper() in text_upper:
                return team
        
        return 'NFL General'


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_all_news_articles(config: Dict) -> pd.DataFrame:
    """Fetch and process all news articles from configured RSS feeds"""
    
    APP_SETTINGS = config.get('app', {})
    NFL_TEAMS = config.get('teams', [])
    RSS_FEED_SOURCES = config.get('rss_feeds', {})
    
    fetcher = RSSFeedFetcher(days_lookback=APP_SETTINGS.get('days_lookback', 7))
    news_items = []
    
    # Fetch from general NFL news sources
    general_feeds = [
        (feed['url'], feed['name'])
        for feed in RSS_FEED_SOURCES.get('general_news', [])
        if feed.get('enabled', True)
    ]
    
    if general_feeds:
        articles = fetcher.fetch_multiple_feeds(general_feeds, max_workers=APP_SETTINGS.get('max_workers', 10))
        
        for article in articles:
            team = NewsDataProcessor.identify_team_from_content(article['title'], NFL_TEAMS)
            news_items.append({
                'team': team,
                'headline': article['title'],
                'link': article['link'],
                'date': article['published'],
                'source': article['source'],
                'summary': article['summary']
            })
    
    # Fetch from team-specific feeds
    team_feeds_dict = RSS_FEED_SOURCES.get('team_feeds', {})
    for team, feeds in team_feeds_dict.items():
        if isinstance(feeds, list):
            team_feed_list = [(url, team) for url in feeds if url]
            articles = fetcher.fetch_multiple_feeds(team_feed_list, max_workers=APP_SETTINGS.get('max_workers', 10))
            
            for article in articles:
                news_items.append({
                    'team': team,
                    'headline': article['title'],
                    'link': article['link'],
                    'date': article['published'],
                    'source': article['source'],
                    'summary': article['summary']
                })
    
    if not news_items:
        return pd.DataFrame()
    
    df = pd.DataFrame(news_items)
    df = NewsDataProcessor.remove_duplicate_articles(df)
    df = df.sort_values('date', ascending=False)
    
    return df
