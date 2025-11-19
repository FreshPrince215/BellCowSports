"""
NFL News & Odds Aggregator - Main Application
Multi-tab Streamlit application for NFL news and betting odds visualization
"""

import streamlit as st
from pathlib import Path
from datetime import datetime, date, timedelta

# Import modules
from modules.config_manager import ConfigManager
from modules.news_fetcher import fetch_all_news_articles
from modules.odds_fetcher import OddsFetcher
from modules.ui_components import UIComponents
from modules.theme_manager import ThemeManager

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="NFL News & Odds Aggregator",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'dark'

if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'News'

# =============================================================================
# LOAD CONFIGURATION
# =============================================================================

config_manager = ConfigManager()
CONFIG = config_manager.load_config()
APP_SETTINGS = CONFIG.get('app', {})

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application logic with tabbed interface"""
    
    # Apply theme styles
    theme_manager = ThemeManager()
    theme_manager.apply_styles()
    
    # Initialize UI components
    ui = UIComponents()
    
    # Render header
    ui.render_header()
    
    # Create tabs
    tab1, tab2 = st.tabs(["📰 NFL News", "📊 Betting Odds"])
    
    # =============================================================================
    # TAB 1: NFL NEWS
    # =============================================================================
    with tab1:
        render_news_tab(ui)
    
    # =============================================================================
    # TAB 2: BETTING ODDS
    # =============================================================================
    with tab2:
        render_odds_tab(ui)

def render_news_tab(ui: UIComponents):
    """Render the NFL News tab"""
    
    # Fetch news data with loading indicator
    with st.spinner('📡 Fetching latest NFL news...'):
        df = fetch_all_news_articles(CONFIG)
    
    # Display metrics
    ui.render_news_metrics(df)
    
    if df.empty:
        st.error("⚠️ No news articles available. Please check your RSS feed configuration.")
        return
    
    # Filters
    st.markdown('<div class="section-title">📰 News Feed</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 2])
    
    with col1:
        st.markdown('<div class="filter-label">Filter by Team</div>', unsafe_allow_html=True)
        selected_team = st.selectbox(
            'Team',
            ['All Teams'] + sorted(df['team'].unique().tolist()),
            label_visibility="collapsed",
            key='team_filter'
        )
    
    with col2:
        st.markdown('<div class="filter-label">Sort By</div>', unsafe_allow_html=True)
        sort_order = st.selectbox(
            'Sort',
            ['Newest First', 'Oldest First'],
            label_visibility="collapsed",
            key='sort_filter'
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_team != 'All Teams':
        filtered_df = filtered_df[filtered_df['team'] == selected_team]
    
    # Apply sorting
    if sort_order == 'Oldest First':
        filtered_df = filtered_df.sort_values('date', ascending=True)
    
    # Display article count
    st.markdown(
        f"<div style='margin: 1.5rem 0 1rem 0; color: var(--text-secondary); font-size: 0.875rem;'>"
        f"Showing <strong>{len(filtered_df)}</strong> articles</div>",
        unsafe_allow_html=True
    )
    
    # Render articles
    if filtered_df.empty:
        st.info("No articles match your filter criteria.")
    else:
        for _, row in filtered_df.iterrows():
            ui.render_news_article(row)

def render_odds_tab(ui: UIComponents):
    """Render the Betting Odds tab"""
    
    st.markdown('<div class="section-title">📊 NFL Betting Odds - This Week</div>', unsafe_allow_html=True)
    
    # Try to get API key from secrets first, then fall back to user input
    secret_api_key = st.secrets.get("ODDS_API_KEY", "")
    
    # Check if we need to fetch (once per day)
    from datetime import datetime, date
    today = date.today()
    last_fetch_date = st.session_state.get('odds_last_fetch_date')
    needs_fetch = last_fetch_date != today
    
    # API Key configuration
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if secret_api_key:
            st.success("✅ Using API key from Streamlit Secrets")
            api_key = secret_api_key
        else:
            api_key = st.text_input(
                "The Odds API Key",
                type="password",
                help="Get your free API key from https://the-odds-api.com",
                key="odds_api_key"
            )
    
    with col2:
        st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
        if last_fetch_date:
            st.info(f"📅 Last updated: {last_fetch_date}")
        else:
            st.info("📅 Not fetched today")
    
    with col3:
        st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
        fetch_button = st.button("🔄 Fetch Odds", use_container_width=True, disabled=not needs_fetch)
    
    if not api_key:
        st.info("👆 Enter your API key from [the-odds-api.com](https://the-odds-api.com) to view betting odds.")
        st.markdown("""
        <div style='background: var(--bg-secondary); padding: 1.5rem; border-radius: 8px; margin-top: 1rem;'>
            <h4 style='color: var(--accent-primary); margin-top: 0;'>How to get started:</h4>
            <ol style='color: var(--text-secondary);'>
                <li>Visit <a href='https://the-odds-api.com' target='_blank'>the-odds-api.com</a></li>
                <li>Sign up for a free account (500 requests/month)</li>
                <li>Copy your API key</li>
                <li>Paste it in the field above</li>
                <li>Odds are fetched automatically once per day</li>
            </ol>
            <p style='color: var(--accent-warning); margin-top: 1rem; font-weight: 600;'>
                ⚡ Smart Caching: Odds are fetched once per day to conserve API credits (500/month free tier)
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Auto-fetch on first load or when button clicked
    if (fetch_button or 'odds_data' not in st.session_state) and needs_fetch:
        with st.spinner('📡 Fetching betting odds...'):
            odds_fetcher = OddsFetcher(api_key)
            games = odds_fetcher.get_nfl_week_games()
            st.session_state.odds_data = games
            st.session_state.odds_last_fetch_date = today
            st.success(f"✅ Odds updated! Next update available: {date.today() + timedelta(days=1)}")
    elif not needs_fetch:
        st.info("ℹ️ Odds already fetched today. Come back tomorrow for fresh data!")
    
    games = st.session_state.get('odds_data', [])
    
    if not games:
        st.warning("⚠️ No games found for this week (Thu-Mon), or there was an error fetching data.")
        return
    
    # Display odds metrics
    ui.render_odds_metrics(games)
    
    # Display games
    st.markdown('<div class="section-title">🎲 Game Odds</div>', unsafe_allow_html=True)
    
    for game in games:
        ui.render_game_card(game)

if __name__ == "__main__":
    main()
