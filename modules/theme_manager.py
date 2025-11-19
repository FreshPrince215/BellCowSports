"""
Theme Manager Module
Handles application theming and CSS styling
"""

import streamlit as st

class ThemeManager:
    """Manages application themes and styling"""
    
    def __init__(self):
        self.theme_mode = st.session_state.get('theme_mode', 'dark')
    
    def get_theme_variables(self) -> str:
        """Generate CSS variables based on current theme mode"""
        
        if self.theme_mode == 'dark':
            return """
            :root {
                --bg-primary: #0f172a;
                --bg-secondary: #1e293b;
                --bg-tertiary: #334155;
                --accent-primary: #3b82f6;
                --accent-secondary: #06b6d4;
                --accent-success: #10b981;
                --accent-warning: #f59e0b;
                --accent-danger: #ef4444;
                --text-primary: #f1f5f9;
                --text-secondary: #94a3b8;
                --border-color: #475569;
                --hover-bg: #2d3748;
            }
            """
        else:
            return """
            :root {
                --bg-primary: #ffffff;
                --bg-secondary: #f8fafc;
                --bg-tertiary: #e2e8f0;
                --accent-primary: #2563eb;
                --accent-secondary: #0891b2;
                --accent-success: #059669;
                --accent-warning: #d97706;
                --accent-danger: #dc2626;
                --text-primary: #1e293b;
                --text-secondary: #64748b;
                --border-color: #cbd5e1;
                --hover-bg: #f1f5f9;
            }
            """
    
    def apply_styles(self):
        """Apply comprehensive CSS styling to the application"""
        theme_vars = self.get_theme_variables()
        
        st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            
            {theme_vars}
            
            * {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }}
            
            .stApp {{
                background-color: var(--bg-primary);
                transition: background-color 0.3s ease;
            }}
            
            .main {{
                background-color: var(--bg-primary);
            }}
            
            .app-header {{
                background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
                border-bottom: 3px solid var(--accent-primary);
                padding: 2rem;
                margin: -2rem -2rem 2rem -2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }}
            
            .header-content {{
                display: flex;
                align-items: center;
                gap: 1.5rem;
            }}
            
            .app-title {{
                font-size: 2rem;
                font-weight: 800;
                color: var(--accent-primary);
                letter-spacing: -0.5px;
            }}
            
            .app-subtitle {{
                font-size: 0.875rem;
                color: var(--text-secondary);
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .status-indicator {{
                display: flex;
                align-items: center;
                gap: 0.75rem;
                font-size: 0.875rem;
                color: var(--accent-success);
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .status-dot {{
                width: 10px;
                height: 10px;
                background: var(--accent-success);
                border-radius: 50%;
                animation: pulse 2s infinite;
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; transform: scale(1); }}
                50% {{ opacity: 0.5; transform: scale(1.1); }}
            }}
            
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }}
            
            .metric-card {{
                background: var(--bg-secondary);
                border-left: 4px solid var(--accent-primary);
                padding: 1.5rem;
                border-radius: 8px;
                transition: all 0.3s ease;
            }}
            
            .metric-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.15);
            }}
            
            .metric-value {{
                font-size: 2.5rem;
                font-weight: 800;
                color: var(--accent-primary);
                line-height: 1;
                margin-bottom: 0.5rem;
            }}
            
            .metric-label {{
                font-size: 0.875rem;
                color: var(--text-secondary);
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 600;
            }}
            
            .news-article {{
                background: var(--bg-secondary);
                border-left: 4px solid var(--accent-secondary);
                padding: 1.5rem;
                margin-bottom: 1rem;
                border-radius: 8px;
                transition: all 0.3s ease;
            }}
            
            .news-article:hover {{
                background: var(--hover-bg);
                border-left-color: var(--accent-primary);
                transform: translateX(4px);
                box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.1);
            }}
            
            .article-header {{
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 1rem;
                flex-wrap: wrap;
            }}
            
            .article-timestamp {{
                font-size: 0.875rem;
                color: var(--accent-success);
                font-weight: 600;
                min-width: 100px;
            }}
            
            .article-team-badge {{
                font-size: 0.75rem;
                background: var(--accent-primary);
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 4px;
                font-weight: 700;
                letter-spacing: 0.5px;
                text-transform: uppercase;
            }}
            
            .article-source {{
                font-size: 0.75rem;
                color: var(--text-secondary);
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-weight: 600;
            }}
            
            .article-headline {{
                font-size: 1.125rem;
                font-weight: 600;
                color: var(--text-primary);
                text-decoration: none;
                display: block;
                line-height: 1.6;
                margin-bottom: 0.75rem;
                transition: color 0.2s ease;
            }}
            
            .article-headline:hover {{
                color: var(--accent-primary);
            }}
            
            .article-summary {{
                font-size: 0.9375rem;
                color: var(--text-secondary);
                line-height: 1.7;
                margin-top: 0.75rem;
            }}
            
            .game-card {{
                background: var(--bg-secondary);
                border: 2px solid var(--border-color);
                border-radius: 12px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                transition: all 0.3s ease;
            }}
            
            .game-card:hover {{
                transform: translateY(-4px);
                box-shadow: 0 12px 24px -6px rgba(0, 0, 0, 0.2);
                border-color: var(--accent-primary);
            }}
            
            .game-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1.5rem;
                padding-bottom: 1rem;
                border-bottom: 2px solid var(--border-color);
            }}
            
            .game-date {{
                font-size: 0.875rem;
                color: var(--text-secondary);
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .game-teams {{
                display: grid;
                grid-template-columns: 1fr auto 1fr;
                gap: 2rem;
                align-items: center;
            }}
            
            .team-section {{
                text-align: center;
            }}
            
            .team-name {{
                font-size: 1.25rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 0.5rem;
            }}
            
            .team-odds {{
                font-size: 1.5rem;
                font-weight: 800;
                color: var(--accent-primary);
                margin-bottom: 0.5rem;
            }}
            
            .team-prob {{
                font-size: 0.875rem;
                color: var(--text-secondary);
                font-weight: 600;
            }}
            
            .vs-divider {{
                font-size: 1.5rem;
                font-weight: 800;
                color: var(--text-secondary);
            }}
            
            .filter-label {{
                font-size: 0.875rem;
                color: var(--text-secondary);
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 0.5rem;
                font-weight: 600;
            }}
            
            .section-title {{
                font-size: 1.25rem;
                color: var(--accent-primary);
                text-transform: uppercase;
                letter-spacing: 1.5px;
                font-weight: 700;
                margin-bottom: 1.5rem;
                padding-bottom: 0.75rem;
                border-bottom: 2px solid var(--border-color);
            }}
            
            .stSelectbox > div > div {{
                background: var(--bg-tertiary);
                border: 2px solid var(--border-color);
                border-radius: 8px;
                color: var(--text-primary);
                font-weight: 500;
            }}
            
            .stButton > button {{
                background: var(--bg-tertiary);
                border: 2px solid var(--accent-primary);
                color: var(--accent-primary);
                border-radius: 8px;
                padding: 0.75rem 1.5rem;
                font-weight: 600;
                font-size: 0.875rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                transition: all 0.3s ease;
            }}
            
            .stButton > button:hover {{
                background: var(--accent-primary);
                color: white;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px -2px rgba(59, 130, 246, 0.5);
            }}
            
            .stTabs [data-baseweb="tab-list"] {{
                gap: 2rem;
                background-color: var(--bg-secondary);
                padding: 1rem;
                border-radius: 8px;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                font-weight: 600;
                font-size: 1rem;
                color: var(--text-secondary);
            }}
            
            .stTabs [aria-selected="true"] {{
                color: var(--accent-primary);
                border-bottom-color: var(--accent-primary);
            }}
            
            ::-webkit-scrollbar {{
                width: 12px;
            }}
            
            ::-webkit-scrollbar-track {{
                background: var(--bg-primary);
            }}
            
            ::-webkit-scrollbar-thumb {{
                background: var(--accent-primary);
                border-radius: 6px;
            }}
            
            ::-webkit-scrollbar-thumb:hover {{
                background: var(--accent-secondary);
            }}
            
            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            header {{visibility: hidden;}}
            .stDeployButton {{display: none;}}
        </style>
        """, unsafe_allow_html=True)
