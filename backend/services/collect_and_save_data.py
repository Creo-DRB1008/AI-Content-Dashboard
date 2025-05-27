#!/usr/bin/env python3
"""
Data Collection and Storage Service

This script handles the RSS data collection pipeline:
1. Collects data from RSS feeds only (Twitter/LinkedIn temporarily disabled)
2. Processes and formats the data
3. Stores it in the database
4. Handles logging and error reporting

Usage:
    python collect_and_save_data.py
    python collect_and_save_data.py --limit 10
    python collect_and_save_data.py --source rss
"""

import sys
import os
import argparse
import logging
from datetime import datetime, timezone

# Add the root directory to the Python path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from collectors.base_collector import DataCollector
from src.models.storage import ContentStorage
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger('collect_data')

def main():
    """Collect data from RSS sources and save it to the database."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Collect data from RSS sources and save it to the database')
    parser.add_argument('--days-ago', type=int, default=7, help='Number of days back to collect data')
    parser.add_argument('--max-results', type=int, default=10, help='Maximum number of results to collect per source')
    args = parser.parse_args()

    days_ago = args.days_ago
    max_results = args.max_results

    try:
        logger.info(f"Starting RSS data collection process (days_ago={days_ago}, max_results={max_results})")

        # Initialize the data collector (RSS only)
        collector = DataCollector()

        # TWITTER COLLECTION - TEMPORARILY COMMENTED OUT
        # logger.info(f"Collecting data from Twitter for the past {days_ago} day(s)")
        # twitter_data = collector.twitter_collector.collect_all_tweets(max_results=max_results, days_ago=days_ago)
        # logger.info(f"Collected {len(twitter_data)} items from Twitter")
        twitter_data = []  # Empty for now

        # LINKEDIN COLLECTION - TEMPORARILY COMMENTED OUT
        # logger.info(f"Collecting data from LinkedIn")
        # try:
        #     linkedin_data = collector.linkedin_collector.collect_all_posts(max_results=max_results)
        #     if not linkedin_data:  # If no data was collected, use simulated data
        #         logger.info("No real LinkedIn data collected, using simulated data instead")
        #         linkedin_data = collector.linkedin_collector.simulate_data(count=max_results)
        #         logger.info(f"Generated {len(linkedin_data)} simulated LinkedIn posts")
        #     else:
        #         logger.info(f"Collected {len(linkedin_data)} real items from LinkedIn")
        # except Exception as e:
        #     logger.error(f"Error collecting LinkedIn data: {str(e)}")
        #     logger.info("Falling back to simulated LinkedIn data")
        #     linkedin_data = collector.linkedin_collector.simulate_data(count=max_results)
        #     logger.info(f"Generated {len(linkedin_data)} simulated LinkedIn posts")
        linkedin_data = []  # Empty for now

        # Collect data from RSS feeds (ACTIVE)
        logger.info(f"Collecting data from RSS feeds for the past {days_ago} day(s)")
        rss_data = collector.rss_collector.collect_all_feeds(days_ago=days_ago)
        logger.info(f"Collected {len(rss_data)} items from RSS feeds")

        # Combine all data
        all_data = {
            'twitter': twitter_data,      # Empty - disabled
            'linkedin': linkedin_data,    # Empty - disabled
            'rss': rss_data,             # Active
            'metadata': {
                'collection_time': datetime.now(timezone.utc).isoformat(),
                'total_items': len(twitter_data) + len(linkedin_data) + len(rss_data),
                'active_sources': ['rss'],
                'disabled_sources': ['twitter', 'linkedin']
            }
        }

        # Save data to a JSON file for inspection
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        filename = f"data/collected_data_{timestamp}.json"
        os.makedirs('data', exist_ok=True)
        collector.save_data(all_data, filename)

        # Save data to the database
        logger.info("Saving RSS data to database")
        summary = ContentStorage.save_all_data(all_data)

        logger.info(f"RSS data collection and storage completed successfully")
        logger.info(f"Summary: {summary}")

        print(f"RSS data collection completed. Total items: {all_data['metadata']['total_items']}")
        print(f"Items saved to database: {summary['total']}")
        print(f"Data also saved to file: {filename}")
        print("Note: Twitter and LinkedIn collection temporarily disabled")

    except Exception as e:
        logger.error(f"Error in data collection process: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
