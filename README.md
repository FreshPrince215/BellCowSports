# 🏈 NFL News & Odds Aggregator

A comprehensive Streamlit application that aggregates NFL news from multiple sources and displays betting odds for upcoming games.

## Features

### 📰 News Tab
- **Multi-source aggregation**: Pulls news from ESPN, NFL.com, Yahoo Sports, CBS Sports, Bleacher Report, and all 32 team official websites
- **Smart filtering**: Filter by team or view all NFL news
- **Deduplication**: Automatically removes duplicate articles
- **Team detection**: Intelligently identifies which team(s) each article is about
- **Real-time updates**: Caches data for 30 minutes, then refreshes automatically
- **Clean summaries**: Article summaries with HTML stripped out

### 📊 Betting Odds Tab
- **Live odds**: Fetches current betting lines from Virginia-legal sportsbooks
- **Week view**: Shows Thursday through Monday games
- **Win probabilities**: Calculates normalized win probabilities from odds
- **Visual design**: Color-coded team displays with odds and probabilities
- **API integration**: Uses The Odds API for reliable data
- **Smart caching**: Fetches once per day to conserve API credits (saves 97% of requests!)

### 🎨 Theme Support
- **Dark mode** (default)
- **Light mode**
- One-click theme toggle

## Project Structure

```
nfl-aggregator/
│
├── app.py                          # Main application entry point
├── config.json                     # Configuration file
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
└── modules/                        # Modular components
    ├── __init__.py                # Module initializer
    ├── config_manager.py          # Configuration loading
    ├── news_fetcher.py            # RSS feed fetching
    ├── odds_fetcher.py            # Odds API integration
    ├── theme_manager.py           # Theme and styling
    └── ui_components.py           # Reusable UI components
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download
```bash
# If using git
git clone <your-repo-url>
cd nfl-aggregator

# Or download and extract the ZIP file
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Get API Key (for Odds feature)
1. Visit [the-odds-api.com](https://the-odds-api.com)
2. Sign up for a free account (500 requests/month)
3. Copy your API key
4. Enter it in the app when viewing the Odds tab

### Step 5: Run the Application
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Configuration

### Modifying News Sources

Edit `config.json` to add/remove news sources or customize settings:

```json
{
  "app": {
    "cache_ttl": 1800,          // Cache duration in seconds
    "days_lookback": 7,         // How many days of news to fetch
    "max_workers": 10           // Parallel fetch workers
  },
  "rss_feeds": {
    "general_news": [
      {
        "name": "Source Name",
        "url": "https://example.com/rss",
        "enabled": true         // Set to false to disable
      }
    ]
  }
}
```

### Adding Custom RSS Feeds

To add a new news source:

1. Open `config.json`
2. Add to the `general_news` array:
```json
{
  "name": "Your Source Name",
  "url": "https://yoursource.com/rss.xml",
  "enabled": true
}
```

### Disabling Team Feeds

To disable specific team feeds, find the team in `config.json` and remove or empty their feed URLs.

## Usage

### News Tab

1. **View all news**: Leave filter on "All Teams"
2. **Filter by team**: Select a specific team from the dropdown
3. **Sort**: Choose "Newest First" (default) or "Oldest First"
4. **Click headlines**: Opens the full article in a new tab

### Odds Tab

1. **Enter API key**: Paste your The Odds API key in the input field
2. **Fetch odds**: Click "Fetch Odds" button
3. **View games**: See all Thursday-Monday games with:
   - American odds (e.g., -150, +200)
   - Win probabilities
   - Color-coded team names

## Customization

### Changing Theme Colors

Edit `modules/theme_manager.py` to customize colors:

```python
def get_theme_variables(self) -> str:
    if self.theme_mode == 'dark':
        return """
        :root {
            --accent-primary: #3b82f6;  // Change this
            --accent-secondary: #06b6d4; // And this
            ...
        }
        """
```

### Adding New Features

The modular structure makes it easy to add features:

1. **New data source**: Create a new fetcher in `modules/`
2. **New tab**: Add to `app.py` main function
3. **New UI component**: Add to `modules/ui_components.py`

## Troubleshooting

### No news articles appearing
- Check your internet connection
- Verify RSS feed URLs in `config.json` are still valid
- Some feeds may be temporarily down

### Odds not loading
- Verify your API key is correct
- Check you haven't exceeded your API rate limit (500/month free tier)
- Ensure the current week has scheduled games

### Theme not changing
- Click the theme toggle button
- If stuck, delete your browser cache for localhost:8501

### Module import errors
```bash
# Ensure you're in the project root directory
cd nfl-aggregator

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## API Rate Limits

**The Odds API Free Tier**:
- 500 requests per month
- Each fetch uses 1 request
- Resets monthly
- Upgrade available for higher limits

## Performance Notes

- News cache: 30 minutes (configurable in `config.json`)
- Parallel fetching: 10 workers (configurable)
- Typical load time: 2-5 seconds for first load, instant after caching

## Contributing

To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Credits

- **News Sources**: ESPN, NFL.com, Yahoo Sports, CBS Sports, Bleacher Report, and team official sites
- **Odds API**: [the-odds-api.com](https://the-odds-api.com)
- **Framework**: Streamlit
- **Icons**: Emoji

## Support

For issues or questions:
1. Check this README
2. Review `config.json` settings
3. Verify all dependencies are installed
4. Check API key validity (for odds)

---

**Enjoy tracking your NFL news and odds! 🏈**
