#!/usr/bin/env python3
"""
Script to initialize the database for the AI Dashboard.
"""
import sys
import os
from datetime import datetime

# Add parent directory to path to import from src
sys.path.append('.')

from src.models.database import init_db
from src.models.content import Content, Category
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger('init_db')

def main():
    """Initialize the database and add sample data."""
    try:
        # Initialize database (create tables)
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialized successfully")
        
        # Add sample data if requested
        if len(sys.argv) > 1 and sys.argv[1] == '--with-samples':
            add_sample_data()
            
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        sys.exit(1)

def add_sample_data():
    """Add sample data to the database."""
    from sqlalchemy.orm import Session
    from src.models.database import SessionLocal
    
    logger.info("Adding sample data...")
    
    # Create a session
    db = SessionLocal()
    
    try:
        # Add sample Twitter content
        twitter_samples = [
            {
                'title': 'The Future of AI in Healthcare',
                'content': 'AI is revolutionizing healthcare with predictive analytics and personalized medicine...',
                'url': 'https://example.com/ai-healthcare',
                'source': 'twitter',
                'source_id': 'tweet1',
                'published_at': datetime.utcnow(),
                'author_name': 'AI Health Expert',
                'likes': 120,
                'shares': 45,
                'comments': 23
            },
            {
                'title': 'Ethics in Artificial Intelligence',
                'content': 'The ethical considerations of AI development are becoming increasingly important...',
                'url': 'https://example.com/ai-ethics',
                'source': 'twitter',
                'source_id': 'tweet4',
                'published_at': datetime.utcnow(),
                'author_name': 'AI Ethics Researcher',
                'likes': 210,
                'shares': 78,
                'comments': 45
            }
        ]
        
        # Add sample LinkedIn content
        linkedin_samples = [
            {
                'title': 'Machine Learning Trends in 2025',
                'content': 'The top machine learning trends to watch for in 2025 include...',
                'url': 'https://example.com/ml-trends',
                'source': 'linkedin',
                'source_id': 'post2',
                'published_at': datetime.utcnow(),
                'author_name': 'ML Specialist',
                'likes': 89,
                'shares': 34,
                'comments': 12
            },
            {
                'title': 'How Companies are Implementing AI',
                'content': 'Leading companies are implementing AI in these innovative ways...',
                'url': 'https://example.com/ai-implementation',
                'source': 'linkedin',
                'source_id': 'post5',
                'published_at': datetime.utcnow(),
                'author_name': 'AI Implementation Consultant',
                'likes': 145,
                'shares': 67,
                'comments': 32
            }
        ]
        
        # Add sample RSS content
        rss_samples = [
            {
                'title': 'New Research in Natural Language Processing',
                'content': 'Researchers have made significant breakthroughs in NLP...',
                'url': 'https://example.com/nlp-research',
                'source': 'rss',
                'source_id': 'article3',
                'published_at': datetime.utcnow(),
                'author_name': 'NLP Research Team',
                'likes': 56,
                'shares': 23,
                'comments': 8
            },
            {
                'title': 'The Role of Deep Learning in Computer Vision',
                'content': 'Deep learning has transformed computer vision applications...',
                'url': 'https://example.com/deep-learning-vision',
                'source': 'rss',
                'source_id': 'article6',
                'published_at': datetime.utcnow(),
                'author_name': 'Computer Vision Expert',
                'likes': 78,
                'shares': 34,
                'comments': 15
            }
        ]
        
        # Combine all samples
        all_samples = twitter_samples + linkedin_samples + rss_samples
        
        # Add to database
        for sample in all_samples:
            content = Content(
                title=sample['title'],
                content=sample['content'],
                url=sample['url'],
                source=sample['source'],
                source_id=sample['source_id'],
                published_at=sample['published_at'],
                author_name=sample['author_name'],
                likes=sample['likes'],
                shares=sample['shares'],
                comments=sample['comments']
            )
            db.add(content)
        
        # Commit changes
        db.commit()
        logger.info(f"Added {len(all_samples)} sample content items to database")
        
    except Exception as e:
        logger.error(f"Error adding sample data: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
