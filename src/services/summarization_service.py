"""
Summarization service for generating article summaries using external APIs.
"""
import requests
import json
import time
from typing import Optional, Dict, Any
import re
from html import unescape

from src.utils.config import (
    SUMMARIZATION_API_KEY, 
    SUMMARIZATION_API_URL, 
    SUMMARIZATION_MODEL,
    SUMMARIZATION_MAX_TOKENS,
    SUMMARIZATION_ENABLED
)
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger('summarization_service')

class SummarizationService:
    """
    Service for generating article summaries using external APIs.
    """
    
    def __init__(self):
        """Initialize the summarization service."""
        self.api_key = SUMMARIZATION_API_KEY
        self.api_url = SUMMARIZATION_API_URL
        self.model = SUMMARIZATION_MODEL
        self.max_tokens = SUMMARIZATION_MAX_TOKENS
        self.enabled = SUMMARIZATION_ENABLED
        
        if not self.api_key and self.enabled:
            logger.warning("Summarization API key not provided. Summarization will be disabled.")
            self.enabled = False
        
        logger.info(f"Summarization service initialized. Enabled: {self.enabled}")
    
    def clean_content(self, content: str) -> str:
        """
        Clean and prepare content for summarization.
        
        Args:
            content (str): Raw content from RSS feed
            
        Returns:
            str: Cleaned content
        """
        if not content:
            return ""
        
        # Unescape HTML entities
        content = unescape(content)
        
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        
        # Remove extra whitespace and newlines
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Limit content length to avoid API limits (keep first 2000 characters)
        if len(content) > 2000:
            content = content[:2000] + "..."
        
        return content
    
    def generate_summary_openai(self, content: str, title: str = "") -> Optional[str]:
        """
        Generate summary using OpenAI API.
        
        Args:
            content (str): Article content to summarize
            title (str): Article title for context
            
        Returns:
            Optional[str]: Generated summary or None if failed
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # Create prompt
            prompt = f"""Please provide a concise summary of the following AI-related article in 2-3 sentences. Focus on the key insights, developments, or findings.

Title: {title}

Content: {content}

Summary:"""
            
            data = {
                'model': self.model,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': self.max_tokens,
                'temperature': 0.3
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                summary = result['choices'][0]['message']['content'].strip()
                logger.debug(f"Generated summary: {summary[:100]}...")
                return summary
            else:
                logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error when calling OpenAI API: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI summarization: {str(e)}")
            return None
    
    def generate_summary_generic(self, content: str, title: str = "") -> Optional[str]:
        """
        Generate summary using a generic API endpoint.
        This method can be adapted for other summarization APIs.
        
        Args:
            content (str): Article content to summarize
            title (str): Article title for context
            
        Returns:
            Optional[str]: Generated summary or None if failed
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'text': content,
                'max_length': self.max_tokens,
                'min_length': 50
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                # Adapt this based on your API's response format
                summary = result.get('summary', result.get('text', ''))
                logger.debug(f"Generated summary: {summary[:100]}...")
                return summary
            else:
                logger.error(f"Summarization API error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error when calling summarization API: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in generic summarization: {str(e)}")
            return None
    
    def generate_summary(self, content: str, title: str = "") -> Optional[str]:
        """
        Generate a summary for the given content.
        
        Args:
            content (str): Article content to summarize
            title (str): Article title for context
            
        Returns:
            Optional[str]: Generated summary or None if failed/disabled
        """
        if not self.enabled:
            logger.debug("Summarization is disabled")
            return None
        
        if not content or len(content.strip()) < 50:
            logger.debug("Content too short for summarization")
            return None
        
        # Clean the content
        cleaned_content = self.clean_content(content)
        
        if not cleaned_content:
            logger.debug("No content after cleaning")
            return None
        
        logger.info(f"Generating summary for article: {title[:50]}...")
        
        # Determine which API to use based on URL
        if 'openai.com' in self.api_url:
            summary = self.generate_summary_openai(cleaned_content, title)
        else:
            summary = self.generate_summary_generic(cleaned_content, title)
        
        if summary:
            logger.info(f"Successfully generated summary ({len(summary)} characters)")
            return summary
        else:
            logger.warning("Failed to generate summary")
            return None
    
    def generate_summaries_batch(self, articles: list) -> Dict[str, str]:
        """
        Generate summaries for multiple articles with rate limiting.
        
        Args:
            articles (list): List of article dictionaries with 'content' and 'title' keys
            
        Returns:
            Dict[str, str]: Dictionary mapping article IDs to summaries
        """
        summaries = {}
        
        for i, article in enumerate(articles):
            article_id = article.get('id', f'article_{i}')
            content = article.get('content', '')
            title = article.get('title', '')
            
            summary = self.generate_summary(content, title)
            if summary:
                summaries[article_id] = summary
            
            # Rate limiting - wait between requests
            if i < len(articles) - 1:  # Don't wait after the last request
                time.sleep(1)  # 1 second delay between requests
        
        logger.info(f"Generated {len(summaries)} summaries out of {len(articles)} articles")
        return summaries


# Global instance
summarization_service = SummarizationService()
