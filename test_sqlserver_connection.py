#!/usr/bin/env python3
"""
Test SQL Server connection for AI Dashboard
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
    """Test the SQL Server connection."""
    try:
        logger.info(f"Testing connection to SQL Server at {DB_HOST}")
        logger.info(f"Database: {DB_NAME}, User: {DB_USER}")
        
        # Create engine
        engine = create_engine(ACTIVE_DATABASE_URL, pool_pre_ping=True)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT @@VERSION as version"))
            version = result.fetchone()
            logger.info(f"Successfully connected to SQL Server!")
            logger.info(f"Server version: {version[0]}")
            
            # Test if database exists
            result = connection.execute(text("SELECT DB_NAME() as current_db"))
            current_db = result.fetchone()
            logger.info(f"Current database: {current_db[0]}")
            
            return True
            
    except Exception as e:
        logger.error(f"Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing SQL Server connection...")
    success = test_connection()
    if success:
        print("✅ SQL Server connection successful!")
    else:
        print("❌ SQL Server connection failed!")
        sys.exit(1) 