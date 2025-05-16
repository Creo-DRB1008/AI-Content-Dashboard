#!/usr/bin/env python3
"""
Script to fetch content from the database and return as JSON.
Used by the Next.js API route.
"""
import json
import sys
import argparse
from datetime import datetime

# Add parent directory to path to import from src
sys.path.append('.')

from src.models.storage import ContentStorage

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Fetch content from the database')
    parser.add_argument('--date', type=str, help='Filter by date (YYYY-MM-DD)')
    parser.add_argument('--source', type=str, help='Filter by source (twitter, linkedin, rss)')
    parser.add_argument('--limit', type=int, default=30, help='Maximum number of items to retrieve')
    parser.add_argument('--get-dates', action='store_true', help='Get available dates instead of content')
    args = parser.parse_args()

    if args.get_dates:
        # Get available dates
        dates = ContentStorage.get_available_dates(limit=args.limit)
        print(json.dumps(dates, default=json_serial))
    else:
        # Get content with optional filters
        content_list = ContentStorage.get_recent_content(
            limit=args.limit,
            source=args.source,
            date=args.date
        )

        # Print as JSON to stdout (will be captured by the API route)
        print(json.dumps(content_list, default=json_serial))

if __name__ == "__main__":
    main()