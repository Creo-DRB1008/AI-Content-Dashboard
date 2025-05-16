"""
Main script for the AI Dashboard data collection.
"""
import argparse
import json
import os
from datetime import datetime

from src.data_collection.collector import DataCollector
from src.models.storage import initialize_database, ContentStorage
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger('main')

def parse_args():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='AI Dashboard Data Collection')
    
    parser.add_argument('--init-db', action='store_true', help='Initialize the database')
    parser.add_argument('--collect', action='store_true', help='Collect data from all sources')
    parser.add_argument('--max-results', type=int, default=100, help='Maximum number of results per source')
    parser.add_argument('--days-ago', type=int, default=7, help='How many days back to collect data')
    parser.add_argument('--save-json', action='store_true', help='Save collected data to JSON file')
    parser.add_argument('--save-db', action='store_true', help='Save collected data to database')
    parser.add_argument('--output-file', type=str, help='Output JSON file path')
    
    return parser.parse_args()

def main():
    """
    Main function.
    """
    args = parse_args()
    
    # Initialize database if requested
    if args.init_db:
        logger.info("Initializing database...")
        initialize_database()
        logger.info("Database initialization completed")
    
    # Collect data if requested
    if args.collect:
        logger.info(f"Collecting data (max_results={args.max_results}, days_ago={args.days_ago})...")
        
        # Create data collector
        collector = DataCollector()
        
        # Collect data
        data = collector.collect_all_data(max_results=args.max_results, days_ago=args.days_ago)
        
        # Save to JSON file if requested
        if args.save_json:
            output_file = args.output_file
            if not output_file:
                timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                output_file = f"data/collected_data_{timestamp}.json"
            
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Save data
            collector.save_data(data, output_file)
            logger.info(f"Data saved to {output_file}")
        
        # Save to database if requested
        if args.save_db:
            logger.info("Saving data to database...")
            summary = ContentStorage.save_all_data(data)
            logger.info(f"Database save summary: {json.dumps(summary)}")
        
        logger.info("Data collection completed")

if __name__ == "__main__":
    main()
