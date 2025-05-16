#!/usr/bin/env python3
"""
Script to collect data from various sources and save it to the database.
This script will:
1. Collect real data from Twitter using the Twitter API
2. Collect real data from LinkedIn using the Lix API
3. Collect real data from RSS feeds
4. Save all collected data to the database

Usage:
    python collect_and_save_data.py [--days-ago DAYS_AGO] [--max-results MAX_RESULTS]

Options:
    --days-ago DAYS_AGO         Number of days back to collect data (default: 7)
    --max-results MAX_RESULTS   Maximum number of results to collect per source (default: 10)
"""
import sys
import os
import argparse
from datetime import datetime, timezone

# Add parent directory to path to import from src
sys.path.append('.')

from src.data_collection.collector import DataCollector
from src.models.storage import ContentStorage
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger('collect_data')

def main():
    """Collect data from various sources and save it to the database."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Collect data from various sources and save it to the database')
    parser.add_argument('--days-ago', type=int, default=7, help='Number of days back to collect data')
    parser.add_argument('--max-results', type=int, default=10, help='Maximum number of results to collect per source')
    args = parser.parse_args()

    days_ago = args.days_ago
    max_results = args.max_results

    try:
        logger.info(f"Starting data collection process (days_ago={days_ago}, max_results={max_results})")

        # Initialize the data collector
        collector = DataCollector()

        # Collect data from Twitter
        logger.info(f"Collecting data from Twitter for the past {days_ago} day(s)")
        twitter_data = collector.twitter_collector.collect_all_tweets(max_results=max_results, days_ago=days_ago)
        logger.info(f"Collected {len(twitter_data)} items from Twitter")

        # Try to collect real data from LinkedIn, fall back to simulated data if it fails
        logger.info(f"Collecting data from LinkedIn")
        try:
            linkedin_data = collector.linkedin_collector.collect_all_posts(max_results=max_results)
            if not linkedin_data:  # If no data was collected, use simulated data
                logger.info("No real LinkedIn data collected, using simulated data instead")
                linkedin_data = collector.linkedin_collector.simulate_data(count=max_results)
                logger.info(f"Generated {len(linkedin_data)} simulated LinkedIn posts")
            else:
                logger.info(f"Collected {len(linkedin_data)} real items from LinkedIn")
        except Exception as e:
            logger.error(f"Error collecting LinkedIn data: {str(e)}")
            logger.info("Falling back to simulated LinkedIn data")
            linkedin_data = collector.linkedin_collector.simulate_data(count=max_results)
            logger.info(f"Generated {len(linkedin_data)} simulated LinkedIn posts")

        # Collect data from RSS feeds
        logger.info(f"Collecting data from RSS feeds for the past {days_ago} day(s)")
        rss_data = collector.rss_collector.collect_all_feeds(days_ago=days_ago)
        logger.info(f"Collected {len(rss_data)} items from RSS feeds")

        # Combine all data
        all_data = {
            'twitter': twitter_data,
            'linkedin': linkedin_data,
            'rss': rss_data,
            'metadata': {
                'collection_time': datetime.now(timezone.utc).isoformat(),
                'total_items': len(twitter_data) + len(linkedin_data) + len(rss_data)
            }
        }

        # Save data to a JSON file for inspection
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
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
