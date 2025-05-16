#!/usr/bin/env python3
"""
Script to clean the database by removing all content.
"""
import sys
import os
from datetime import datetime

# Add parent directory to path to import from src
sys.path.append('.')

from src.models.database import get_db, init_db
from src.models.content import Content
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger('clean_database')

def main():
    """Clean the database by removing all content."""
    try:
        logger.info("Starting database cleaning process")
        
        # Get database session
        db = next(get_db())
        
        try:
            # Count existing records
            count = db.query(Content).count()
            logger.info(f"Found {count} records in the database")
            
            # Delete all records
            db.query(Content).delete()
            db.commit()
            
            logger.info(f"Successfully deleted {count} records from the database")
            print(f"Successfully deleted {count} records from the database")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error cleaning database: {str(e)}")
            print(f"Error: {str(e)}")
            sys.exit(1)
        finally:
            db.close()
        
    except Exception as e:
        logger.error(f"Error connecting to database: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
