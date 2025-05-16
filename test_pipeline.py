"""
Test script for the entire data collection pipeline.
"""
import os
import json
from datetime import datetime

# Modify the database configuration to use SQLite for testing
os.environ["DATABASE_URL"] = "sqlite:///pipeline_test.db"

# Override the database configuration in the config module
import src.utils.config as config
config.DATABASE_URL = "sqlite:///pipeline_test.db"

def test_full_pipeline():
    print("\n=== Testing Full Data Collection Pipeline ===")

    try:
        # Step 1: Initialize the database
        print("\nStep 1: Initializing database...")
        from src.models.storage import initialize_database
        initialize_database()
        print("Database initialized successfully")

        # Step 2: Collect data
        print("\nStep 2: Collecting data...")
        from src.data_collection.collector import DataCollector

        collector = DataCollector()
        data = collector.collect_all_data(max_results=5, days_ago=3)

        print(f"Collected data summary:")
        print(f"- Twitter: {len(data['twitter'])} items")
        print(f"- LinkedIn: {len(data['linkedin'])} items")
        print(f"- RSS: {len(data['rss'])} items")
        print(f"- Total: {data['metadata']['total_items']} items")

        # Step 3: Save data to JSON
        print("\nStep 3: Saving data to JSON...")
        output_file = f"data/pipeline_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        collector.save_data(data, output_file)
        print(f"Data saved to {output_file}")

        # Step 4: Save data to database
        print("\nStep 4: Saving data to database...")
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

        print("\nFull pipeline test completed successfully")
        return True
    except Exception as e:
        print(f"Error testing full pipeline: {str(e)}")
        return False
    finally:
        # Clean up test database
        try:
            os.remove("pipeline_test.db")
            print("\nTest database removed")
        except:
            print("\nFailed to remove test database")

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    # Run the test
    test_full_pipeline()
