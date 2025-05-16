#!/usr/bin/env python3
"""
Script to collect data from various sources and save it to the database.
This script will:
1. Collect real data from Twitter using the Twitter API
2. Collect real data from LinkedIn using the Lix API
3. Collect real data from RSS feeds
4. Save all collected data to the database
"""
import sys
import os
from datetime import datetime

# Add parent directory to path to import from src
sys.path.append('.')

from src.data_collection.collector import DataCollector
from src.models.storage import ContentStorage
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger('collect_data')

def main():
    """Collect data from various sources and save it to the database."""
    try:
        logger.info("Starting data collection process")

        # Initialize the data collector
        collector = DataCollector()

        # Collect data from Twitter
        logger.info("Collecting data from Twitter")
        twitter_data = collector.twitter_collector.collect_all_tweets(max_results=10, days_ago=7)
        logger.info(f"Collected {len(twitter_data)} items from Twitter")

        # Try to collect real data from LinkedIn, fall back to simulated data if it fails
        logger.info("Collecting data from LinkedIn")
        try:
            linkedin_data = collector.linkedin_collector.collect_all_posts(max_results=10)
            if not linkedin_data:  # If no data was collected, use simulated data
                logger.info("No real LinkedIn data collected, using simulated data instead")
                linkedin_data = collector.linkedin_collector.simulate_data(count=10)
                logger.info(f"Generated {len(linkedin_data)} simulated LinkedIn posts")
            else:
                logger.info(f"Collected {len(linkedin_data)} real items from LinkedIn")
        except Exception as e:
            logger.error(f"Error collecting LinkedIn data: {str(e)}")
            logger.info("Falling back to simulated LinkedIn data")
            linkedin_data = collector.linkedin_collector.simulate_data(count=10)
            logger.info(f"Generated {len(linkedin_data)} simulated LinkedIn posts")

        # Collect data from RSS feeds
        logger.info("Collecting data from RSS feeds")
        rss_data = collector.rss_collector.collect_all_feeds(days_ago=7)
        logger.info(f"Collected {len(rss_data)} items from RSS feeds")

        # Combine all data
        all_data = {
            'twitter': twitter_data,
            'linkedin': linkedin_data,
            'rss': rss_data,
            'metadata': {
                'collection_time': datetime.utcnow().isoformat(),
                'total_items': len(twitter_data) + len(linkedin_data) + len(rss_data)
            }
        }

        # Save data to a JSON file for inspection
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"data/collected_data_{timestamp}.json"
        os.makedirs('data', exist_ok=True)
        collector.save_data(all_data, filename)

        # Save data to the database
        logger.info("Saving data to database")
        summary = ContentStorage.save_all_data(all_data)

        logger.info(f"Data collection and storage completed successfully")
        logger.info(f"Summary: {summary}")

        print(f"Data collection completed. Total items: {all_data['metadata']['total_items']}")
        print(f"Items saved to database: {summary['total']}")
        print(f"Data also saved to file: {filename}")

    except Exception as e:
        logger.error(f"Error in data collection process: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
