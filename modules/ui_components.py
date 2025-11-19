"""
UI Components Module
Reusable UI components for the application
"""

import streamlit as st
import pandas as pd
from typing import Dict, List
from modules.odds_fetcher import OddsFetcher

class UIComponents:
    """Reusable UI components"""
    
    def render_header(self):
        """Render the application header with theme toggle"""
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("""
            <div class="app-header">
                <div class="header-content">
                    <div>
                        <div class="app-title">🏈 NFL News & Odds Aggregator</div>
                        <div class="app-subtitle">Real-Time News & Betting Analysis</div>
                    </div>
                </div>
                <div>
                    <div class="status-indicator">
                        <div class="status-dot"></div>
                        LIVE
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("🌓 Toggle Theme", use_container_width=True):
                st.session_state.theme_mode = 'light' if st.session_state.theme_mode == 'dark' else 'dark'
                st.rerun()
    
    def render_news_metrics(self, df: pd.DataFrame):
        """Render metrics dashboard for news"""
        if df.empty:
            return
        
        total_articles = len(df)
        teams_covered = df['team'].nunique()
        sources_count = df['source'].nunique()
        
        st.markdown(f"""
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">{total_articles}</div>
                <div class="metric-label">Total Articles</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{teams_covered}</div>
                <div class="metric-label">Teams Covered</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{sources_count}</div>
                <div class="metric-label">News Sources</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_odds_metrics(self, games: List[Dict]):
        """Render metrics dashboard for odds"""
        if not games:
            return
        
        total_games = len(games)
        
        # Count favorites vs underdogs
        favorites = sum(1 for g in games if g['h_odds'] < 0 or g['a_odds'] < 0)
        
        st.markdown(f"""
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">{total_games}</div>
                <div class="metric-label">Games This Week</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{favorites}</div>
                <div class="metric-label">Games with Favorites</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_news_article(self, row: pd.Series):
        """Render individual news article card"""
        date_str = row['date'].strftime('%b %d, %Y %I:%M %p EST')
        
        summary_html = f"<div class='article-summary'>{row['summary']}</div>" if row['summary'] else ""
        
        st.markdown(f"""
        <div class="news-article">
            <div class="article-header">
                <span class="article-timestamp">{date_str}</span>
                <span class="article-team-badge">{row['team']}</span>
                <span class="article-source">{row['source']}</span>
            </div>
            <a href="{row['link']}" target="_blank" class="article-headline">
                {row['headline']}
            </a>
            {summary_html}
        </div>
        """, unsafe_allow_html=True)
    
    def render_game_card(self, game: Dict):
        """Render individual game card with odds"""
        
        # Calculate true probabilities (with vig removed)
        away_prob, home_prob = OddsFetcher.remove_vig(game['a_odds'], game['h_odds'])
        
        # Format odds
        away_odds_str = OddsFetcher.format_odds(game['a_odds'])
        home_odds_str = OddsFetcher.format_odds(game['h_odds'])
        
        # Extract team nicknames
        away_nickname = game['away'].split()[-1]
        home_nickname = game['home'].split()[-1]
        
        # Format date
        date_str = game['start_time'].strftime('%A, %B %d, %Y')
        
        st.markdown(f"""
        <div class="game-card">
            <div class="game-header">
                <div class="game-date">📅 {date_str}</div>
            </div>
            <div class="game-teams">
                <div class="team-section">
                    <div class="team-name" style="color: {game['a_col']}">{away_nickname}</div>
                    <div class="team-odds">{away_odds_str}</div>
                    <div class="team-prob">{away_prob:.1f}% Win Probability</div>
                </div>
                <div class="vs-divider">@</div>
                <div class="team-section">
                    <div class="team-name" style="color: {game['h_col']}">{home_nickname}</div>
                    <div class="team-odds">{home_odds_str}</div>
                    <div class="team-prob">{home_prob:.1f}% Win Probability</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
