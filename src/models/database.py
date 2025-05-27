"""
Database connection module for the AI Dashboard.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.utils.config import ACTIVE_DATABASE_URL
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger('database')

# Create SQLAlchemy engine with SQL Server specific settings
try:
    # SQL Server specific engine configuration
    engine_kwargs = {}
    if 'mssql' in ACTIVE_DATABASE_URL:
        engine_kwargs.update({
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'echo': False
        })
    
    engine = create_engine(ACTIVE_DATABASE_URL, **engine_kwargs)
    logger.info(f"Database engine created successfully for: {ACTIVE_DATABASE_URL.split('@')[0]}@***")
except Exception as e:
    logger.error(f"Error creating database engine: {str(e)}")
    raise

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db():
    """
    Get a database session.
    
    Yields:
        Session: A SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database by creating all tables.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise
