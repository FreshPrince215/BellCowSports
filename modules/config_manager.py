"""
Configuration Manager Module
Handles loading and validation of application configuration
"""

import json
import streamlit as st
from pathlib import Path
from typing import Dict

class ConfigManager:
    """Manages application configuration loading and validation"""
    
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file
        self.config_path = Path(__file__).parent.parent / config_file
    
    @st.cache_resource
    def load_config(_self) -> Dict:
        """Load application configuration from JSON file"""
        
        if not _self.config_path.exists():
            st.error("⚠️ Configuration file not found. Please ensure config.json exists.")
            st.stop()
        
        try:
            with open(_self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                _self._validate_config(config)
                return config
        except json.JSONDecodeError as e:
            st.error(f"❌ Invalid JSON in configuration file: {e}")
            st.stop()
        except Exception as e:
            st.error(f"❌ Error loading configuration: {e}")
            st.stop()
    
    def _validate_config(self, config: Dict) -> None:
        """Validate configuration structure"""
        required_keys = ['app', 'teams', 'rss_feeds']
        
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required configuration key: {key}")
        
        if not isinstance(config['teams'], list):
            raise ValueError("'teams' must be a list")
        
        if not isinstance(config['rss_feeds'], dict):
            raise ValueError("'rss_feeds' must be a dictionary")
