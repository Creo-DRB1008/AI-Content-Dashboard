#!/usr/bin/env python3
"""
Test the RSS data collection and storage pipeline with SQL Server.

This script tests:
1. RSS data collection only (Twitter/LinkedIn temporarily disabled)
2. Data processing and formatting
3. SQL Server database storage
4. Data retrieval

Usage:
    python test_pipeline.py

Note: This script uses the configured SQL Server database from environment variables.
Make sure your .env file has the correct SQL Server configuration.
"""

import sys
import json
import os
from datetime import datetime

# Set up the path to import modules
sys.path.insert(0, '.')

def test_full_pipeline():
    print("\n=== Testing RSS Data Collection Pipeline ===")

    try:
        # Step 1: Initialize the database
        print("\nStep 1: Initializing database...")
        from src.models.storage import initialize_database
        initialize_database()
        print("Database initialized successfully")

        # Step 2: Collect data (RSS only)
        print("\nStep 2: Collecting RSS data only...")
        from collectors.base_collector import DataCollector

        collector = DataCollector()
        data = collector.collect_all_data(max_results=5, days_ago=3)

        print(f"Collected data summary:")
        print(f"- Twitter: {len(data['twitter'])} items (disabled)")
        print(f"- LinkedIn: {len(data['linkedin'])} items (disabled)")
        print(f"- RSS: {len(data['rss'])} items (active)")
        print(f"- Total: {data['metadata']['total_items']} items")
        print(f"- Active sources: {data['metadata']['active_sources']}")
        print(f"- Disabled sources: {data['metadata']['disabled_sources']}")

        # Step 3: Save data to JSON
        print("\nStep 3: Saving data to JSON...")
        output_file = f"data/pipeline_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        collector.save_data(data, output_file)
        print(f"Data saved to {output_file}")

        # Step 4: Save data to database
        print("\nStep 4: Saving RSS data to database...")
        from src.models.storage import ContentStorage

        summary = ContentStorage.save_all_data(data)
        print(f"Database save summary: {json.dumps(summary)}")

        # Step 5: Retrieve data from database
        print("\nStep 5: Retrieving data from database...")
        recent = ContentStorage.get_recent_content(limit=10)
        print(f"Retrieved {len(recent)} recent content items")

        # Print a sample item
        if recent:
            print("\nSample content item:")
            sample = recent[0]
            for key, value in sample.items():
                print(f"- {key}: {value}")

        print("\nRSS pipeline test completed successfully")
        print("Note: Twitter and LinkedIn collection temporarily disabled")
        return True
    except Exception as e:
        print(f"Error testing RSS pipeline: {str(e)}")
        return False
    finally:
        # Note: SQL Server database cleanup is not needed as we use the main database
        print("\nPipeline test completed. SQL Server database remains intact.")

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    print("RSS Data Collection Pipeline Test")
    print("Twitter and LinkedIn collection temporarily disabled")

    # Run the test
    test_full_pipeline()
