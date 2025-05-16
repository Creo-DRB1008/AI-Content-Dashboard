"""
Test script for database models and storage.
"""
import os
import json
from datetime import datetime
import sqlite3

# Modify the database configuration to use SQLite for testing
os.environ["DATABASE_URL"] = "sqlite:///test_ai_dashboard.db"

# Override the database configuration in the config module
import src.utils.config as config
config.DATABASE_URL = "sqlite:///test_ai_dashboard.db"

def test_database_connection():
    print("\n=== Testing Database Connection ===")
    try:
        from src.models.database import engine, Base, init_db

        # Create tables
        Base.metadata.create_all(bind=engine)

        print("Successfully connected to database and created tables")
        return True
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return False

def test_category_model():
    print("\n=== Testing Category Model ===")
    try:
        from src.models.database import engine, SessionLocal, Base
        from src.models.content import Category

        # Create tables
        Base.metadata.create_all(bind=engine)

        # Create a session
        db = SessionLocal()

        try:
            # Create test categories
            categories = [
                Category(name="Test Research", description="Test research category"),
                Category(name="Test Product", description="Test product category")
            ]

            # Add to database
            db.add_all(categories)
            db.commit()

            # Query categories
            db_categories = db.query(Category).all()
            print(f"Created {len(db_categories)} test categories")

            return True
        except Exception as e:
            db.rollback()
            print(f"Error testing Category model: {str(e)}")
            return False
        finally:
            db.close()
    except Exception as e:
        print(f"Error setting up database session: {str(e)}")
        return False

def test_content_model():
    print("\n=== Testing Content Model ===")
    try:
        from src.models.database import engine, SessionLocal, Base
        from src.models.content import Content, Category

        # Create tables
        Base.metadata.create_all(bind=engine)

        # Create a session
        db = SessionLocal()

        try:
            # Get a category
            category = db.query(Category).first()

            if not category:
                print("No categories found, creating one")
                category = Category(name="Test Category", description="Test category")
                db.add(category)
                db.commit()

            # Create test content
            content = Content(
                title="Test Content",
                content="This is a test content item",
                url="https://example.com/test",
                source="test",
                source_id="test-123",
                published_at=datetime.now(),  # Using now() instead of utcnow()
                author_name="Test Author"
            )

            # Add to database
            db.add(content)
            db.commit()

            # Add category to content
            content.categories.append(category)
            db.commit()

            # Query content
            db_content = db.query(Content).filter(Content.source_id == "test-123").first()

            if db_content:
                print(f"Created test content: {db_content.title}")
                print(f"Categories: {[c.name for c in db_content.categories]}")
                return True
            else:
                print("Failed to retrieve test content")
                return False
        except Exception as e:
            db.rollback()
            print(f"Error testing Content model: {str(e)}")
            return False
        finally:
            db.close()
    except Exception as e:
        print(f"Error setting up database session: {str(e)}")
        return False

def test_storage_module():
    print("\n=== Testing Storage Module ===")
    try:
        from src.models.storage import ContentStorage, initialize_database

        # Initialize database
        initialize_database()

        # Create test data
        twitter_data = [
            {
                "id": "test-twitter-1",
                "text": "This is a test tweet",
                "created_at": datetime.utcnow().isoformat(),
                "likes": 10,
                "retweets": 5,
                "replies": 2,
                "url": "https://twitter.com/test/status/1",
                "author": {
                    "id": "test-user-1",
                    "username": "testuser",
                    "name": "Test User"
                }
            }
        ]

        linkedin_data = [
            {
                "id": "test-linkedin-1",
                "text": "This is a test LinkedIn post",
                "created_at": datetime.utcnow().isoformat(),
                "likes": 20,
                "shares": 3,
                "comments": 5,
                "url": "https://linkedin.com/post/1",
                "author": {
                    "id": "test-user-2",
                    "name": "Test LinkedIn User",
                    "profile_url": "https://linkedin.com/in/testuser"
                }
            }
        ]

        rss_data = [
            {
                "id": "test-rss-1",
                "title": "Test RSS Entry",
                "content": "This is a test RSS entry",
                "link": "https://example.com/rss/1",
                "published": datetime.utcnow().isoformat(),
                "author": "Test RSS Author"
            }
        ]

        # Create combined data
        data = {
            "twitter": twitter_data,
            "linkedin": linkedin_data,
            "rss": rss_data
        }

        # Save to database
        summary = ContentStorage.save_all_data(data)

        print(f"Storage test summary: {json.dumps(summary)}")

        # Retrieve recent content
        recent = ContentStorage.get_recent_content(limit=10)
        print(f"Retrieved {len(recent)} recent content items")

        return True
    except Exception as e:
        print(f"Error testing storage module: {str(e)}")
        return False

# Run all tests
def run_all_tests():
    tests = {
        "Database Connection": test_database_connection,
        "Category Model": test_category_model,
        "Content Model": test_content_model,
        "Storage Module": test_storage_module
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

    # Clean up test database
    try:
        os.remove("test_ai_dashboard.db")
        print("\nTest database removed")
    except:
        print("\nFailed to remove test database")

if __name__ == "__main__":
    run_all_tests()
