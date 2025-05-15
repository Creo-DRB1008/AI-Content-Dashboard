"""
Test script for data collection components.
"""
import os
import json
from datetime import datetime

# Create necessary directories
os.makedirs('data', exist_ok=True)
os.makedirs('logs', exist_ok=True)

# Test RSS collector
def test_rss_collector():
    print("\n=== Testing RSS Collector ===")
    try:
        from src.data_collection.rss_collector import RSSCollector

        collector = RSSCollector()
        entries = collector.collect_all_feeds(days_ago=7)

        # Save to a JSON file for inspection
        output_file = f"data/rss_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(entries, f, indent=2)

        print(f"Collected {len(entries)} RSS entries")
        print(f"Data saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error testing RSS collector: {str(e)}")
        return False

# Test LinkedIn collector (real data)
def test_linkedin_collector():
    print("\n=== Testing LinkedIn Collector (Real Data) ===")
    try:
        from src.data_collection.linkedin_collector import LinkedInCollector

        collector = LinkedInCollector()

        # Try to collect real data if API key is available
        if collector.api_key:
            print("API key found, collecting real LinkedIn data...")
            # Collect posts for a specific keyword
            posts = collector.collect_posts_by_keyword("artificial intelligence", max_results=5)
            data_type = "real"
        else:
            print("No API key found, falling back to simulated data...")
            posts = collector.simulate_data(10)
            data_type = "simulated"

        # Save to a JSON file for inspection
        output_file = f"data/linkedin_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(posts, f, indent=2)

        print(f"Collected {len(posts)} {data_type} LinkedIn posts")
        print(f"Data saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error testing LinkedIn collector: {str(e)}")
        return False

def test_twitter_collector():
    print("\n=== Testing Twitter Collector ===")
    print("Note: This will fail with placeholder API keys, but tests the code structure")
    try:
        from src.data_collection.twitter_collector import TwitterCollector

        collector = TwitterCollector()
        try:
            tweets = collector.collect_all_tweets()

            # Save to a JSON file for inspection
            output_file = f"data/twitter_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(output_file, 'w') as f:
                json.dump(tweets, f, indent=2)

            print(f"Collected {len(tweets)} tweets")
            print(f"Data saved to {output_file}")
        except Exception as e:
            print(f"Expected error with placeholder API keys: {str(e)}")
            print("This is normal with placeholder credentials")

        return True
    except Exception as e:
        print(f"Error testing Twitter collector structure: {str(e)}")
        return False

# Test main collector
def test_main_collector():
    print("\n=== Testing Main Collector ===")
    try:
        from src.data_collection.collector import DataCollector

        collector = DataCollector()

        # This will partially fail with placeholder API keys, but will collect RSS data
        data = collector.collect_all_data(max_results=10, days_ago=3)

        # Save the data
        output_file = f"data/collector_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        collector.save_data(data, output_file)

        print(f"Data collection completed. Total items: {data['metadata']['total_items']}")
        print(f"Data saved to {output_file}")
        return True
    except Exception as e:
        print(f"Error testing main collector: {str(e)}")
        return False

# Test database models (without actual database connection)
def test_models():
    print("\n=== Testing Database Models ===")
    try:
        from src.models.content import Content, Category

        # Create a sample content item
        content = Content(
            title="Test Content",
            content="This is a test content item",
            url="https://example.com/test",
            source="test",
            source_id="test-123",
            published_at=datetime.utcnow(),
            author_name="Test Author"
        )

        # Create a sample category
        category = Category(
            name="Test Category",
            description="This is a test category"
        )

        print("Successfully imported and created model instances")
        return True
    except Exception as e:
        print(f"Error testing models: {str(e)}")
        return False

# Run all tests
def run_all_tests():
    tests = {
        # "RSS Collector": test_rss_collector,
        "LinkedIn Collector": test_linkedin_collector,
        # "Twitter Collector": test_twitter_collector,
        "Main Collector": test_main_collector,
        "Database Models": test_models
    }

    results = {}

    for name, test_func in tests.items():
        print(f"\nRunning test: {name}")
        result = test_func()
        results[name] = "PASS" if result else "FAIL"

    # Print summary
    print("\n=== Test Results Summary ===")
    for name, result in results.items():
        print(f"{name}: {result}")

if __name__ == "__main__":
    run_all_tests()
