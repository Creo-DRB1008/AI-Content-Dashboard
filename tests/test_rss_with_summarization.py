#!/usr/bin/env python3
"""
Test script for RSS collection with summarization.
"""
import sys
import os
import json

# Add the root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collectors.rss_collector import RSSCollector
from src.models.storage import ContentStorage
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger('test_rss_summarization')

def test_rss_collection_with_summarization():
    """Test RSS collection with summarization enabled."""
    print("\n=== Testing RSS Collection with Summarization ===")
    
    try:
        # Create RSS collector with a limited set of feeds for testing
        test_feeds = {
            'venturebeat_ai': 'https://venturebeat.com/category/ai/feed/',
            'techcrunch_ai': 'https://techcrunch.com/tag/artificial-intelligence/feed/'
        }
        
        collector = RSSCollector(feeds=test_feeds)
        
        # Collect a small number of recent articles
        print("Collecting RSS articles with summarization...")
        entries = collector.collect_all_feeds(days_ago=3)
        
        if not entries:
            print("⚠️ No entries collected. This might be normal if feeds are empty.")
            return True
        
        print(f"Collected {len(entries)} entries")
        
        # Check if summaries were generated
        summarized_count = 0
        for entry in entries:
            if entry.get('summary'):
                summarized_count += 1
                print(f"✅ Summary generated for: {entry['title'][:50]}...")
                print(f"   Summary: {entry['summary'][:100]}...")
            else:
                print(f"⚠️ No summary for: {entry['title'][:50]}...")
        
        print(f"\nSummaries generated: {summarized_count}/{len(entries)}")
        
        # Save sample data for inspection
        sample_file = 'data/rss_with_summaries_test.json'
        os.makedirs('data', exist_ok=True)
        with open(sample_file, 'w') as f:
            json.dump(entries[:3], f, indent=2)  # Save first 3 entries
        
        print(f"Sample data saved to: {sample_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing RSS collection with summarization: {str(e)}")
        return False

def test_database_storage_with_summaries():
    """Test storing RSS articles with summaries in the database."""
    print("\n=== Testing Database Storage with Summaries ===")
    
    try:
        # Create sample RSS data with summaries
        sample_data = {
            'twitter': [],
            'linkedin': [],
            'rss': [
                {
                    'id': 'test-rss-summary-1',
                    'title': 'Test Article with AI Summary',
                    'link': 'https://example.com/test-article-1',
                    'published': '2025-05-27T12:00:00',
                    'content': 'This is a test article about artificial intelligence developments. It contains detailed information about recent breakthroughs in machine learning and their applications in various industries.',
                    'summary': 'AI researchers have made significant breakthroughs in machine learning with applications across multiple industries.',
                    'source': 'rss',
                    'feed_name': 'test_feed',
                    'author': 'Test Author'
                }
            ]
        }
        
        # Save to database
        print("Saving test data with summaries to database...")
        summary = ContentStorage.save_all_data(sample_data)
        
        print(f"Saved {summary['total']} items to database")
        
        # Retrieve and verify
        print("Retrieving content from database...")
        content_list = ContentStorage.get_recent_content(limit=5)
        
        # Check if summaries are preserved
        summary_found = False
        for item in content_list:
            if item.get('summary'):
                summary_found = True
                print(f"✅ Summary found in database: {item['summary'][:100]}...")
                break
        
        if summary_found:
            print("✅ Summaries are properly stored and retrieved from database")
            return True
        else:
            print("⚠️ No summaries found in retrieved content")
            return False
        
    except Exception as e:
        print(f"❌ Error testing database storage with summaries: {str(e)}")
        return False

def test_end_to_end_pipeline():
    """Test the complete pipeline from RSS collection to database storage."""
    print("\n=== Testing End-to-End Pipeline ===")
    
    try:
        # Use a single reliable feed for testing
        test_feeds = {
            'venturebeat_ai': 'https://venturebeat.com/category/ai/feed/'
        }
        
        collector = RSSCollector(feeds=test_feeds)
        
        # Collect articles
        print("Step 1: Collecting RSS articles...")
        entries = collector.collect_all_feeds(days_ago=1)  # Just 1 day to limit results
        
        if not entries:
            print("⚠️ No entries collected for end-to-end test")
            return True
        
        print(f"Collected {len(entries)} entries")
        
        # Prepare data for storage
        all_data = {
            'twitter': [],
            'linkedin': [],
            'rss': entries[:2]  # Limit to 2 entries for testing
        }
        
        # Save to database
        print("Step 2: Saving to database...")
        summary = ContentStorage.save_all_data(all_data)
        
        print(f"Saved {summary['total']} items to database")
        
        # Retrieve and display
        print("Step 3: Retrieving from database...")
        content_list = ContentStorage.get_recent_content(limit=3)
        
        print("Retrieved content:")
        for item in content_list:
            print(f"- Title: {item['title'][:50]}...")
            if item.get('summary'):
                print(f"  Summary: {item['summary'][:80]}...")
            else:
                print(f"  Content: {item['content'][:80]}...")
            print(f"  URL: {item['url']}")
            print()
        
        print("✅ End-to-end pipeline test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error in end-to-end pipeline test: {str(e)}")
        return False

def main():
    """Run all RSS summarization tests."""
    print("RSS Collection with Summarization Test Suite")
    print("=" * 50)
    
    tests = [
        ("RSS Collection with Summarization", test_rss_collection_with_summarization),
        ("Database Storage with Summaries", test_database_storage_with_summaries),
        ("End-to-End Pipeline", test_end_to_end_pipeline)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\nRunning test: {test_name}")
        result = test_func()
        results[test_name] = "PASS" if result else "FAIL"
    
    # Print summary
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    for test_name, result in results.items():
        status_icon = "✅" if result == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {result}")
    
    # Overall result
    all_passed = all(result == "PASS" for result in results.values())
    if all_passed:
        print("\n🎉 All tests passed!")
        print("\nNext steps:")
        print("1. Add your summarization API key to .env file")
        print("2. Run the data collection pipeline")
        print("3. Check the frontend to see summaries in action")
    else:
        print("\n⚠️ Some tests failed. Check your configuration.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
