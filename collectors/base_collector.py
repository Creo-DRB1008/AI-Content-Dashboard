#!/usr/bin/env python3
"""
Main data collection module for the AI Dashboard.
"""
import json
import os
from datetime import datetime

# from .twitter_collector import TwitterCollector        # Temporarily commented out
# from .linkedin_collector import LinkedInCollector      # Temporarily commented out
from .rss_collector import RSSCollector
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger('main_collector')

class DataCollector:
    """
    Main data collection class that aggregates data from all sources.
    """

    def __init__(self):
        """
        Initialize the data collector with all source collectors.
        """
        # self.twitter_collector = TwitterCollector()        # Temporarily commented out
        # self.linkedin_collector = LinkedInCollector()      # Temporarily commented out
        self.rss_collector = RSSCollector()

        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)

        logger.info("Data collector initialized (RSS only)")

    def collect_all_data(self, max_results=100, days_ago=7):
        """
        Collect data from all sources.

        Args:
            max_results (int): Maximum number of items to retrieve per source.
            days_ago (int): How many days back to search.

        Returns:
            dict: Dictionary containing data from all sources.
        """
        logger.info(f"Starting data collection from RSS sources only (max_results={max_results}, days_ago={days_ago})")

        # Collect data from Twitter - TEMPORARILY COMMENTED OUT
        # try:
        #     twitter_data = self.twitter_collector.collect_all_tweets(max_results, days_ago)
        #     logger.info(f"Collected {len(twitter_data)} items from Twitter")
        # except Exception as e:
        #     logger.error(f"Error collecting Twitter data: {str(e)}")
        #     twitter_data = []
        twitter_data = []  # Empty for now

        # Collect data from LinkedIn - TEMPORARILY COMMENTED OUT
        # try:
        #     # Check if we have an API key for LinkedIn
        #     if self.linkedin_collector.api_key:
        #         # Use real LinkedIn data
        #         linkedin_data = self.linkedin_collector.collect_all_posts(max_results)
        #         logger.info(f"Collected {len(linkedin_data)} items from LinkedIn (real data)")
        #     else:
        #         # Fall back to simulated data if no API key is available
        #         linkedin_data = self.linkedin_collector.simulate_data(max_results)
        #         logger.info(f"Collected {len(linkedin_data)} items from LinkedIn (simulated)")
        # except Exception as e:
        #     logger.error(f"Error collecting LinkedIn data: {str(e)}")
        #     linkedin_data = []
        linkedin_data = []  # Empty for now

        # Collect data from RSS feeds
        try:
            rss_data = self.rss_collector.collect_all_feeds(days_ago)
            logger.info(f"Collected {len(rss_data)} items from RSS feeds")
        except Exception as e:
            logger.error(f"Error collecting RSS data: {str(e)}")
            rss_data = []

        # Combine all data
        all_data = {
            'twitter': twitter_data,      # Empty for now
            'linkedin': linkedin_data,    # Empty for now
            'rss': rss_data,
            'metadata': {
                'collection_time': datetime.utcnow().isoformat(),
                'max_results': max_results,
                'days_ago': days_ago,
                'total_items': len(twitter_data) + len(linkedin_data) + len(rss_data),
                'active_sources': ['rss'],  # Only RSS is active
                'disabled_sources': ['twitter', 'linkedin']  # Temporarily disabled
            }
        }

        logger.info(f"Data collection completed. Total items: {all_data['metadata']['total_items']} (RSS only)")
        return all_data

    def save_data(self, data, filename=None):
        """
        Save collected data to a JSON file.

        Args:
            data (dict): Data to save.
            filename (str): Optional filename. If not provided, a timestamp-based name is used.

        Returns:
            str: Path to the saved file.
        """
        if filename is None:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f"data/collected_data_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"Data saved to {filename}")
        return filename


# For testing
if __name__ == "__main__":
    collector = DataCollector()

    # Collect data from all sources (RSS only for now)
    data = collector.collect_all_data(max_results=10, days_ago=3)

    # Save the data
    collector.save_data(data)

    print(f"Data collection completed. Total items: {data['metadata']['total_items']} (RSS only)")
