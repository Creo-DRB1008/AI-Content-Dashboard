"""
Configuration utilities for the AI Dashboard.
"""
import os
from dotenv import load_dotenv
import urllib.parse

# Load environment variables from .env file
load_dotenv()

# Twitter API Configuration
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

# LinkedIn API Configuration
LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID', '')
LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET', '')
LINKEDIN_API_KEY = os.getenv('LINKEDIN_API_KEY', '')  # API key for third-party service

# Summarization API Configuration
SUMMARIZATION_API_KEY = os.getenv('SUMMARIZATION_API_KEY', '')
SUMMARIZATION_API_URL = os.getenv('SUMMARIZATION_API_URL', 'https://api.openai.com/v1/chat/completions')
SUMMARIZATION_MODEL = os.getenv('SUMMARIZATION_MODEL', 'gpt-3.5-turbo')
SUMMARIZATION_MAX_TOKENS = int(os.getenv('SUMMARIZATION_MAX_TOKENS', '150'))
SUMMARIZATION_ENABLED = os.getenv('SUMMARIZATION_ENABLED', 'true').lower() == 'true'

# Database Configuration - SQL Server only
# Remove SQLite fallback, use SQL Server exclusively
DATABASE_URL = os.getenv('DATABASE_URL', '')

# SQL Server Database Configuration (individual parameters)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '1433')
DB_NAME = os.getenv('DB_NAME', 'ai_dashboard')
DB_USER = os.getenv('DB_USER', '')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

# Function to build SQL Server connection string
def get_sqlserver_connection_string():
    """Build SQL Server connection string from environment variables."""
    # Ensure all required SQL Server parameters are provided
    if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME]):
        raise ValueError("Missing required SQL Server database configuration. Please set DB_HOST, DB_USER, DB_PASSWORD, and DB_NAME environment variables.")

    # Use URL encoding for special characters in password
    encoded_password = urllib.parse.quote_plus(DB_PASSWORD)
    # Use TDS 7.3 which works successfully
    return f"mssql+pyodbc://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}?driver=FreeTDS&TDS_Version=7.3"

# Use the SQL Server database URL exclusively
ACTIVE_DATABASE_URL = get_sqlserver_connection_string()

# Twitter search parameters
TWITTER_AI_HASHTAGS = [
    '#artificialintelligence',
    # '#machinelearning',
    # '#deeplearning',
    # '#nlp',
    # '#computervision',
    # '#llm',
    # '#generativeai'
]

TWITTER_KEY_ACCOUNTS = [
    'OpenAI',
    # 'AnthropicAI',
    # 'GoogleAI',
    # 'MetaAI',
    # 'DeepMind',
    # 'StabilityAI',
    # 'Midjourney'
]

# RSS Feed URLs
RSS_FEEDS = {
    'wired_ai': 'https://www.wired.com/feed/tag/artificial-intelligence/latest/rss',
    'mit_ai': 'https://news.mit.edu/topic/artificial-intelligence2-rss.xml',
    'google_ai': 'https://ai.googleblog.com/feeds/posts/default',
    'nvidia_ai': 'https://blogs.nvidia.com/blog/category/ai/feed/',
    'venturebeat_ai': 'https://venturebeat.com/category/ai/feed/',
    'techcrunch_ai': 'https://techcrunch.com/tag/artificial-intelligence/feed/',
    'microsoft_ai': 'https://techcommunity.microsoft.com/gxcuf89792/rss/board?board.id=AI_Blog',
    'ibm_ai': 'https://research.ibm.com/blog/rss',
    'technologyreview_ai': 'https://www.technologyreview.com/feed/topic/artificial-intelligence/',
    # 'arxiv_ai': 'https://export.arxiv.org/rss/cs.AI',
    # 'arxiv_lg': 'https://export.arxiv.org/rss/cs.LG',
    'deepmind_ai': 'https://www.deepmind.com/blog/rss.xml',
    'openai_blog': 'https://openai.com/blog/rss',
    'theaireport': 'https://theaireport.substack.com/feed',
    'jack_clark': 'https://jack-clark.net/index.xml',
    'bair_berkeley': 'https://bair.berkeley.edu/blog/feed.xml',
    'thegradient': 'https://thegradient.pub/rss/'
}
