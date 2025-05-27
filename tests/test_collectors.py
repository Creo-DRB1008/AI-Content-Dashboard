#!/usr/bin/env python3
"""
Test script for data collectors

Usage:
    python test_collectors.py [collector_type]
    
    collector_type: 'rss', 'all' (default)
    Note: Twitter and LinkedIn tests are temporarily disabled

Example:
    python test_collectors.py rss
    python test_collectors.py all
"""

import sys
import os
import json
from datetime import datetime

# Add the root directory to the Python path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create necessary directories
os.makedirs('data', exist_ok=True)
os.makedirs('logs', exist_ok=True)

# Test RSS Collector
from collectors.rss_collector import RSSCollector

def test_rss_collector():
    print("=== Testing RSS Collector ===")
    
    # Create RSS collector (it uses default feeds from config)
    collector = RSSCollector()
    
    try:
        # Fetch latest content from all configured feeds
        content = collector.collect_all_feeds(days_ago=3)
        
        print(f"Successfully fetched {len(content)} articles from RSS feeds")
        for i, item in enumerate(content[:3]):  # Show first 3 items
            print(f"- {item['title'][:50]}... (from {item['feed_name']})")
        
        return True
    except Exception as e:
        print(f"RSS Collector test failed: {e}")
        return False

# LINKEDIN COLLECTOR TEST - TEMPORARILY COMMENTED OUT
# from collectors.linkedin_collector import LinkedInCollector
# 
# def test_linkedin_collector():
#     print("\n=== Testing LinkedIn Collector ===")
#     
#     collector = LinkedInCollector()
#     
#     # Test data sources
#     test_queries = [
#         "artificial intelligence",
#         "machine learning",
#         "AI"
#     ]
#     
#     try:
#         for query in test_queries:
#             content = collector.fetch_content(query=query, limit=2)
#             print(f"Query '{query}': Found {len(content)} posts")
#             
#             for item in content:
#                 print(f"- {item['title'][:50]}...")
#         
#         return True
#     except Exception as e:
#         print(f"LinkedIn Collector test failed: {e}")
#         return False

# TWITTER COLLECTOR TEST - TEMPORARILY COMMENTED OUT
# from collectors.twitter_collector import TwitterCollector
# 
# def test_twitter_collector():
#     print("\n=== Testing Twitter Collector ===")
#     
#     collector = TwitterCollector()
#     
#     # Test queries
#     test_queries = [
#         "#ArtificialIntelligence",
#         "#MachineLearning", 
#         "#AI"
#     ]
#     
#     try:
#         for query in test_queries:
#             content = collector.fetch_content(query=query, limit=2)
#             print(f"Query '{query}': Found {len(content)} tweets")
#             
#             for item in content:
#                 print(f"- {item['title'][:50]}...")
#         
#         return True
#     except Exception as e:
#         print(f"Twitter Collector test failed: {e}")
#         return False

# Test DataCollector (main collector) - RSS only
from collectors.base_collector import DataCollector

def test_main_collector():
    print("\n=== Testing Main Collector (RSS only) ===")
    try:
        collector = DataCollector()

        # This will collect RSS data only
        data = collector.collect_all_data(max_results=10, days_ago=3)

        # Save the data
        output_file = f"data/collector_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        collector.save_data(data, output_file)

        print(f"RSS data collection completed. Total items: {data['metadata']['total_items']}")
        print(f"RSS items: {len(data['rss'])}")
        print(f"Data saved to {output_file}")
        print("Note: Twitter and LinkedIn collectors are temporarily disabled")
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

# Run all tests (RSS only)
def run_all_tests():
    tests = {
        "RSS Collector": test_rss_collector,
        # "LinkedIn Collector": test_linkedin_collector,    # Temporarily disabled
        # "Twitter Collector": test_twitter_collector,      # Temporarily disabled
        "Main Collector (RSS only)": test_main_collector,
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
    
    print("\nNote: Twitter and LinkedIn tests are temporarily disabled")

if __name__ == "__main__":
    print("AI Content Dashboard Test Suite (RSS only)")
    print("Twitter and LinkedIn collectors are temporarily disabled")
    run_all_tests()
