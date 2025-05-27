#!/usr/bin/env python3
"""
Test database connection for AI Dashboard
"""
import sys
import os
from sqlalchemy import create_engine, text

# Add the root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils.config import ACTIVE_DATABASE_URL, DB_HOST, DB_USER, DB_NAME
from src.utils.logger import setup_logger

logger = setup_logger('test_connection')

def test_connection():
    """Test the database connection."""
    try:
        logger.info(f"Testing connection to database at {DB_HOST}")
        logger.info(f"Database: {DB_NAME}, User: {DB_USER}")
        logger.info(f"Connection URL: {ACTIVE_DATABASE_URL.split('@')[0]}@***")
        
        # Create engine
        engine = create_engine(ACTIVE_DATABASE_URL, pool_pre_ping=True)
        
        # Test connection
        with engine.connect() as connection:
            # Use appropriate SQL for the database type
            if 'mssql' in ACTIVE_DATABASE_URL:
                result = connection.execute(text("SELECT @@VERSION as version"))
                version = result.fetchone()
                logger.info(f"Successfully connected to SQL Server!")
                logger.info(f"Server version: {version[0]}")
                
        # Test database name in a separate connection
        with engine.connect() as connection:
            if 'mssql' in ACTIVE_DATABASE_URL:
                result = connection.execute(text("SELECT DB_NAME() as current_db"))
                current_db = result.fetchone()
                logger.info(f"Current database: {current_db[0]}")
            else:
                # SQLite or other database
                result = connection.execute(text("SELECT 'Connected to database' as status"))
                status = result.fetchone()
                logger.info(f"Successfully connected to database!")
                logger.info(f"Status: {status[0]}")
        
        return True
        
    except Exception as e:
        logger.error(f"Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing database connection...")
    success = test_connection()
    if success:
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed!")
        sys.exit(1) 