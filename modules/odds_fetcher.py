"""
Odds Fetcher Module
Handles fetching and processing NFL betting odds from The Odds API
"""

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class OddsFetcher:
    """Fetches and processes NFL betting odds"""
    
    # NFL team colors for visualization
    TEAM_COLORS = {
        "Arizona Cardinals": "#97233F",
        "Atlanta Falcons": "#A71930",
        "Baltimore Ravens": "#241773",
        "Buffalo Bills": "#00338D",
        "Carolina Panthers": "#0085CA",
        "Chicago Bears": "#0B162A",
        "Cincinnati Bengals": "#FB4F14",
        "Cleveland Browns": "#FF3C00",
        "Dallas Cowboys": "#003594",
        "Denver Broncos": "#FB4F14",
        "Detroit Lions": "#0076B6",
        "Green Bay Packers": "#203731",
        "Houston Texans": "#03202F",
        "Indianapolis Colts": "#002C5F",
        "Jacksonville Jaguars": "#006778",
        "Kansas City Chiefs": "#E31837",
        "Las Vegas Raiders": "#000000",
        "Los Angeles Chargers": "#002A5E",
        "Los Angeles Rams": "#003594",
        "Miami Dolphins": "#008E97",
        "Minnesota Vikings": "#4F2683",
        "New England Patriots": "#002244",
        "New Orleans Saints": "#D3BC8D",
        "New York Giants": "#0B2265",
        "New York Jets": "#125740",
        "Philadelphia Eagles": "#004C54",
        "Pittsburgh Steelers": "#FFB612",
        "San Francisco 49ers": "#AA0000",
        "Seattle Seahawks": "#002244",
        "Tampa Bay Buccaneers": "#D50A0A",
        "Tennessee Titans": "#0C2340",
        "Washington Commanders": "#5A1414",
    }
    
    # Virginia-legal sportsbooks
    VA_LEGAL_BOOKS = ["fanduel", "draftkings", "betmgm", "caesars", "bet365"]
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.the-odds-api.com/v4"
    
    def get_nfl_week_games(self) -> List[Dict]:
        """Fetch NFL games for the current week (Thursday through Monday)"""
        
        url = f"{self.base_url}/sports/americanfootball_nfl/odds"
        params = {
            "apiKey": self.api_key,
            "regions": "us,us2",
            "markets": "h2h",
            "oddsFormat": "american"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching odds: {e}")
            return []
        except ValueError as e:
            print(f"Error parsing JSON: {e}")
            return []
        
        # Calculate Thursday-Monday window
        today = datetime.utcnow().date()
        days_until_thursday = (3 - today.weekday()) % 7
        if days_until_thursday == 0 and today.weekday() != 3:
            days_until_thursday = 7
        thursday = today + timedelta(days=days_until_thursday)
        monday = thursday + timedelta(days=4)
        
        games = []
        for event in data:
            try:
                start = datetime.fromisoformat(event["commence_time"].replace("Z", "+00:00")).date()
            except (KeyError, ValueError) as e:
                print(f"Error parsing event time: {e}")
                continue
            
            if thursday <= start <= monday:
                home = event.get("home_team", "Unknown")
                away = event.get("away_team", "Unknown")
                
                # Virginia-legal books (first available)
                va_odds = {"home": None, "away": None}
                
                for book in event.get("bookmakers", []):
                    if book.get("key") in self.VA_LEGAL_BOOKS:
                        markets = book.get("markets", [])
                        if not markets:
                            continue
                        
                        for outcome in markets[0].get("outcomes", []):
                            price = outcome.get("price")
                            name = outcome.get("name")
                            
                            if name == home and va_odds["home"] is None:
                                va_odds["home"] = price
                            if name == away and va_odds["away"] is None:
                                va_odds["away"] = price
                
                if va_odds["home"] is not None and va_odds["away"] is not None:
                    games.append({
                        "away": away,
                        "a_odds": va_odds["away"],
                        "home": home,
                        "h_odds": va_odds["home"],
                        "a_col": self.TEAM_COLORS.get(away, "#666666"),
                        "h_col": self.TEAM_COLORS.get(home, "#666666"),
                        "start_time": start
                    })
        
        # Sort by start time
        games.sort(key=lambda x: x['start_time'])
        
        return games
    
    @staticmethod
    def odds_to_prob(odds: int) -> float:
        """Convert American odds to probability"""
        if odds > 0:
            return 100 / (odds + 100)
        else:
            return abs(odds) / (abs(odds) + 100)
    
    @staticmethod
    def normalize_probabilities(away_odds: int, home_odds: int) -> tuple:
        """Normalize probabilities to sum to 100%"""
        pa = OddsFetcher.odds_to_prob(away_odds)
        ph = OddsFetcher.odds_to_prob(home_odds)
        total = pa + ph
        return (pa / total * 100, ph / total * 100)
    
    @staticmethod
    def format_odds(odds: int) -> str:
        """Format odds with + or - sign"""
        if odds > 0:
            return f"+{odds}"
        return str(odds)
