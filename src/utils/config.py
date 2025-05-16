"""
Configuration utilities for the AI Dashboard.
"""
import os
from dotenv import load_dotenv

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

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ai_dashboard.db')

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
    'google_ai': 'https://blog.google/technology/ai/rss/',
    'openai_blog': 'https://openai.com/blog/rss.xml'
}
