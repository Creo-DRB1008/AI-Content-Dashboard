#!/usr/bin/env python3
"""
Script to clean the SQL Server database by removing all content.
This script is designed to work exclusively with SQL Server.
"""
import sys

# Add parent directory to path to import from src
sys.path.append('.')

from src.models.database import get_db
from src.models.content import Content, Category
from src.utils.logger import setup_logger
from src.utils.config import ACTIVE_DATABASE_URL

# Set up logger
logger = setup_logger('clean_database')

def main():
    """Clean the SQL Server database by removing all content."""
    try:
        logger.info("Starting SQL Server database cleaning process")
        logger.info(f"Database URL: {ACTIVE_DATABASE_URL.split('@')[0]}@***")

        # Verify we're using SQL Server
        if 'mssql' not in ACTIVE_DATABASE_URL:
            error_msg = "This script is designed to work only with SQL Server. Please check your database configuration."
            logger.error(error_msg)
            print(f"Error: {error_msg}")
            sys.exit(1)

        # Get database session
        db = next(get_db())

        try:
            # Count existing records
            content_count = db.query(Content).count()
            category_count = db.query(Category).count()

            logger.info(f"Found {content_count} content records and {category_count} category records in the database")
            print(f"Found {content_count} content records and {category_count} category records in the database")

            if content_count == 0 and category_count == 0:
                logger.info("Database is already clean")
                print("Database is already clean")
                return

            # Clear many-to-many relationships first by removing all content items
            # This will automatically clear the content_category association table
            if content_count > 0:
                # Get all content items and clear their category relationships
                content_items = db.query(Content).all()
                for content_item in content_items:
                    content_item.categories.clear()
                db.commit()
                logger.info("Cleared all content-category relationships")

                # Now delete all content records
                deleted_content = db.query(Content).delete()
                db.commit()
                logger.info(f"Deleted {deleted_content} content records")
                print(f"Deleted {deleted_content} content records")

            # Delete all category records
            if category_count > 0:
                deleted_categories = db.query(Category).delete()
                db.commit()
                logger.info(f"Deleted {deleted_categories} category records")
                print(f"Deleted {deleted_categories} category records")

            # Verify cleanup
            final_content_count = db.query(Content).count()
            final_category_count = db.query(Category).count()

            if final_content_count == 0 and final_category_count == 0:
                logger.info("Database successfully cleaned - all records removed")
                print("Database successfully cleaned - all records removed")
            else:
                logger.warning(f"Cleanup incomplete: {final_content_count} content and {final_category_count} category records remain")
                print(f"Warning: Cleanup incomplete: {final_content_count} content and {final_category_count} category records remain")

        except Exception as e:
            db.rollback()
            logger.error(f"Error cleaning database: {str(e)}")
            print(f"Error cleaning database: {str(e)}")
            sys.exit(1)
        finally:
            db.close()

    except Exception as e:
        logger.error(f"Error connecting to SQL Server database: {str(e)}")
        print(f"Error connecting to SQL Server database: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
