#!/usr/bin/env python3
"""
Script to view the data in the database.
"""
import sys
import json
from datetime import datetime

# Add parent directory to path to import from src
sys.path.append('.')

from src.models.storage import ContentStorage
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger('view_database')

def main():
    """View the data in the database."""
    try:
        # Get content from database
        content = ContentStorage.get_recent_content(limit=50)
        
        # Print summary
        print(f"Found {len(content)} items in the database")
        
        # Count by source
        sources = {}
        for item in content:
            source = item['source']
            sources[source] = sources.get(source, 0) + 1
        
        print("\nItems by source:")
        for source, count in sources.items():
            print(f"  {source}: {count}")
        
        # Print sample items
        print("\nSample items:")
        for i, item in enumerate(content[:5]):
            print(f"\n--- Item {i+1} ---")
            print(f"Title: {item['title']}")
            print(f"Source: {item['source']}")
            print(f"URL: {item['url']}")
            print(f"Published: {item['published_at']}")
            
            # Truncate content for display
            content_text = item['content']
            if content_text and len(content_text) > 100:
                content_text = content_text[:100] + "..."
            print(f"Content: {content_text}")
        
        # Save to JSON file for inspection
        with open('database_content.json', 'w') as f:
            json.dump(content, f, indent=2)
        
        print(f"\nFull data saved to database_content.json")
        
    except Exception as e:
        logger.error(f"Error viewing database: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
