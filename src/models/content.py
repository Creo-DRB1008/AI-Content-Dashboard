"""
Content models for the AI Dashboard.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from src.models.database import Base

# Association table for content-category many-to-many relationship
content_category = Table(
    'content_category',
    Base.metadata,
    Column('content_id', String(36), ForeignKey('content.id')),
    Column('category_id', Integer, ForeignKey('category.id'))
)

class Content(Base):
    """
    Unified content model for all data sources.
    """
    __tablename__ = 'content'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=True)
    url = Column(String(512), nullable=False)
    source = Column(String(50), nullable=False)  # twitter, linkedin, rss
    source_id = Column(String(255), nullable=True)  # Original ID from the source
    published_at = Column(DateTime, nullable=False, default=datetime.now)
    collected_at = Column(DateTime, nullable=False, default=datetime.now)

    # Engagement metrics
    likes = Column(Integer, nullable=True)
    shares = Column(Integer, nullable=True)
    comments = Column(Integer, nullable=True)

    # Author information
    author_name = Column(String(255), nullable=True)
    author_url = Column(String(512), nullable=True)
    author_image_url = Column(String(512), nullable=True)

    # AI processing fields
    summary = Column(Text, nullable=True)
    sentiment_score = Column(Float, nullable=True)

    # Relationships
    categories = relationship('Category', secondary=content_category, back_populates='content_items')

    def __repr__(self):
        return f"<Content(id='{self.id}', source='{self.source}', title='{self.title}')>"

    @classmethod
    def from_twitter(cls, tweet_data):
        """
        Create a Content instance from Twitter data.

        Args:
            tweet_data (dict): Twitter data.

        Returns:
            Content: A Content instance.
        """
        content = cls(
            source='twitter',
            source_id=str(tweet_data.get('id')),
            content=tweet_data.get('text'),
            url=tweet_data.get('url'),
            published_at=datetime.fromisoformat(tweet_data.get('created_at')),
            likes=tweet_data.get('likes'),
            shares=tweet_data.get('retweets'),
            comments=tweet_data.get('replies')
        )

        # Add author information if available
        if 'author' in tweet_data:
            author = tweet_data['author']
            content.author_name = author.get('name') or author.get('username')
            content.author_url = f"https://twitter.com/{author.get('username')}"
            content.author_image_url = author.get('profile_image_url')

        return content

    @classmethod
    def from_linkedin(cls, linkedin_data):
        """
        Create a Content instance from LinkedIn data.

        Args:
            linkedin_data (dict): LinkedIn data.

        Returns:
            Content: A Content instance.
        """
        content = cls(
            source='linkedin',
            source_id=str(linkedin_data.get('id')),
            content=linkedin_data.get('text'),
            url=linkedin_data.get('url'),
            published_at=datetime.fromisoformat(linkedin_data.get('created_at')),
            likes=linkedin_data.get('likes'),
            shares=linkedin_data.get('shares'),
            comments=linkedin_data.get('comments')
        )

        # Add author information if available
        if 'author' in linkedin_data:
            author = linkedin_data['author']
            content.author_name = author.get('name')
            content.author_url = author.get('profile_url')

        return content

    @classmethod
    def from_rss(cls, rss_data):
        """
        Create a Content instance from RSS data.

        Args:
            rss_data (dict): RSS data.

        Returns:
            Content: A Content instance.
        """
        content = cls(
            source='rss',
            source_id=str(rss_data.get('id')),
            title=rss_data.get('title'),
            content=rss_data.get('content'),
            url=rss_data.get('link'),
            published_at=datetime.fromisoformat(rss_data.get('published')),
            author_name=rss_data.get('author'),
            summary=rss_data.get('summary')  # Add summary field
        )

        return content


class Category(Base):
    """
    Content category model.
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    # Relationships
    content_items = relationship('Content', secondary=content_category, back_populates='categories')

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
