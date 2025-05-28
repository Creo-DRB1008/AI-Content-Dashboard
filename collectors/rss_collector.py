"""
RSS feed aggregator module for the AI Dashboard.
"""
import feedparser
import json
from datetime import datetime, timedelta
import time
from dateutil import parser as date_parser

from src.utils.config import RSS_FEEDS
from src.utils.logger import setup_logger
from src.services.summarization_service import summarization_service

# Set up logger
logger = setup_logger('rss_collector')

class RSSCollector:
    """
    Collects AI-related content from RSS feeds.
    """

    def __init__(self, feeds=None):
        """
        Initialize the RSS collector with feed URLs.

        Args:
            feeds (dict): Dictionary of feed names and URLs.
        """
        self.feeds = feeds or RSS_FEEDS
        logger.info(f"RSS collector initialized with {len(self.feeds)} feeds")

    def parse_feed(self, feed_url, feed_name, days_ago=7):
        """
        Parse a single RSS feed and extract relevant entries.

        Args:
            feed_url (str): URL of the RSS feed.
            feed_name (str): Name of the feed for identification.
            days_ago (int): How many days back to include entries.

        Returns:
            list: List of parsed entries.
        """
        logger.info(f"Parsing RSS feed: {feed_name} ({feed_url})")

        try:
            # Parse the feed
            feed = feedparser.parse(feed_url)

            if not feed.entries:
                logger.warning(f"No entries found in feed: {feed_name}")
                return []

            # Calculate cutoff date
            cutoff_date = datetime.now() - timedelta(days=days_ago)

            entries = []
            for entry in feed.entries:
                # Extract publication date
                if hasattr(entry, 'published'):
                    try:
                        pub_date = date_parser.parse(entry.published)
                        # Ensure timezone awareness consistency
                        if pub_date.tzinfo is not None:
                            pub_date = pub_date.replace(tzinfo=None)
                    except:
                        # If date parsing fails, use current time
                        pub_date = datetime.now()
                elif hasattr(entry, 'updated'):
                    try:
                        pub_date = date_parser.parse(entry.updated)
                        # Ensure timezone awareness consistency
                        if pub_date.tzinfo is not None:
                            pub_date = pub_date.replace(tzinfo=None)
                    except:
                        pub_date = datetime.now()
                else:
                    # No date available, use current time
                    pub_date = datetime.now()

                # Skip entries older than cutoff date - both are now timezone naive
                if pub_date < cutoff_date:
                    continue

                # Extract content
                content = ""
                if hasattr(entry, 'content'):
                    content = entry.content[0].value
                elif hasattr(entry, 'summary'):
                    content = entry.summary
                elif hasattr(entry, 'description'):
                    content = entry.description

                # Generate summary for the content
                summary = None
                try:
                    summary = summarization_service.generate_summary(content, entry.title)
                except Exception as e:
                    logger.warning(f"Failed to generate summary for entry {entry.title}: {str(e)}")

                # Create entry object
                entry_data = {
                    'id': entry.get('id', entry.link),
                    'title': entry.title,
                    'link': entry.link,
                    'published': pub_date.isoformat(),
                    'content': content,
                    'summary': summary,  # Add the generated summary
                    'source': 'rss',
                    'feed_name': feed_name,
                    'author': entry.get('author', feed.feed.get('title', feed_name))
                }

                entries.append(entry_data)

            logger.info(f"Parsed {len(entries)} entries from feed: {feed_name}")
            return entries

        except Exception as e:
            logger.error(f"Error parsing feed {feed_name}: {str(e)}")
            return []

    def collect_all_feeds(self, days_ago=7):
        """
        Collect entries from all configured RSS feeds.

        Args:
            days_ago (int): How many days back to include entries.

        Returns:
            list: List of all collected entries.
        """
        all_entries = []

        for feed_name, feed_url in self.feeds.items():
            entries = self.parse_feed(feed_url, feed_name, days_ago)
            all_entries.extend(entries)

            # Add a small delay between requests to be nice to servers
            time.sleep(1)

        logger.info(f"Collected {len(all_entries)} entries from all RSS feeds")
        return all_entries


# For testing
if __name__ == "__main__":
    collector = RSSCollector()
    entries = collector.collect_all_feeds(days_ago=7)

    # Save to a JSON file for inspection
    with open('rss_data_sample.json', 'w') as f:
        json.dump(entries, f, indent=2)

    print(f"Collected {len(entries)} RSS entries")
