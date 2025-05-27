"""
Storage module for the AI Dashboard.
"""
import json
from datetime import datetime
from sqlalchemy.orm import Session

from src.models.database import get_db, init_db
from src.models.content import Content, Category
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger('storage')

class ContentStorage:
    """
    Storage class for content data.
    """

    @staticmethod
    def save_twitter_data(db: Session, tweets):
        """
        Save Twitter data to the database.

        Args:
            db (Session): Database session.
            tweets (list): List of tweet data.

        Returns:
            int: Number of tweets saved.
        """
        count = 0
        for tweet in tweets:
            try:
                # Check if tweet already exists
                existing = db.query(Content).filter(
                    Content.source == 'twitter',
                    Content.source_id == str(tweet.get('id'))
                ).first()

                if existing:
                    logger.debug(f"Tweet {tweet.get('id')} already exists in database")
                    continue

                # Create new content item
                content = Content.from_twitter(tweet)
                db.add(content)
                count += 1
            except Exception as e:
                logger.error(f"Error saving tweet {tweet.get('id')}: {str(e)}")

        db.commit()
        logger.info(f"Saved {count} new tweets to database")
        return count

    @staticmethod
    def save_linkedin_data(db: Session, posts):
        """
        Save LinkedIn data to the database.

        Args:
            db (Session): Database session.
            posts (list): List of LinkedIn post data.

        Returns:
            int: Number of posts saved.
        """
        count = 0
        for post in posts:
            try:
                # Check if post already exists
                existing = db.query(Content).filter(
                    Content.source == 'linkedin',
                    Content.source_id == str(post.get('id'))
                ).first()

                if existing:
                    logger.debug(f"LinkedIn post {post.get('id')} already exists in database")
                    continue

                # Create new content item
                content = Content.from_linkedin(post)
                db.add(content)
                count += 1
            except Exception as e:
                logger.error(f"Error saving LinkedIn post {post.get('id')}: {str(e)}")

        db.commit()
        logger.info(f"Saved {count} new LinkedIn posts to database")
        return count

    @staticmethod
    def save_rss_data(db: Session, entries):
        """
        Save RSS data to the database.

        Args:
            db (Session): Database session.
            entries (list): List of RSS entry data.

        Returns:
            int: Number of entries saved.
        """
        count = 0
        for entry in entries:
            try:
                # Check if entry already exists
                existing = db.query(Content).filter(
                    Content.source == 'rss',
                    Content.source_id == str(entry.get('id'))
                ).first()

                if existing:
                    logger.debug(f"RSS entry {entry.get('id')} already exists in database")
                    continue

                # Create new content item
                content = Content.from_rss(entry)
                db.add(content)
                count += 1
            except Exception as e:
                logger.error(f"Error saving RSS entry {entry.get('id')}: {str(e)}")

        db.commit()
        logger.info(f"Saved {count} new RSS entries to database")
        return count

    @staticmethod
    def save_all_data(data):
        """
        Save all collected data to the database.

        Args:
            data (dict): Dictionary containing data from all sources.

        Returns:
            dict: Summary of saved items.
        """
        db = next(get_db())

        try:
            # Save Twitter data
            twitter_count = ContentStorage.save_twitter_data(db, data.get('twitter', []))

            # Save LinkedIn data
            linkedin_count = ContentStorage.save_linkedin_data(db, data.get('linkedin', []))

            # Save RSS data
            rss_count = ContentStorage.save_rss_data(db, data.get('rss', []))

            summary = {
                'twitter': twitter_count,
                'linkedin': linkedin_count,
                'rss': rss_count,
                'total': twitter_count + linkedin_count + rss_count,
                'timestamp': datetime.utcnow().isoformat()
            }

            logger.info(f"Saved {summary['total']} new items to database")
            return summary

        except Exception as e:
            logger.error(f"Error saving data to database: {str(e)}")
            db.rollback()
            raise
        finally:
            db.close()

    @staticmethod
    def get_recent_content(limit=50, source=None, date=None):
        """
        Get recent content from the database.

        Args:
            limit (int): Maximum number of items to retrieve.
            source (str): Optional source filter.
            date (str): Optional date filter in ISO format (YYYY-MM-DD).

        Returns:
            list: List of content items.
        """
        db = next(get_db())

        try:
            query = db.query(Content).order_by(Content.published_at.desc())

            if source:
                query = query.filter(Content.source == source)

            if date:
                # Convert date string to datetime objects for start and end of day
                from datetime import datetime, timedelta
                try:
                    date_obj = datetime.fromisoformat(date)
                    start_of_day = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
                    end_of_day = start_of_day + timedelta(days=1)

                    # Filter content published on the specified date
                    query = query.filter(Content.published_at >= start_of_day,
                                         Content.published_at < end_of_day)
                except ValueError:
                    logger.error(f"Invalid date format: {date}")

            items = query.limit(limit).all()

            # Convert to dictionaries
            result = []
            for item in items:
                item_dict = {
                    'id': item.id,
                    'title': item.title,
                    'content': item.content,
                    'url': item.url,
                    'source': item.source,
                    'published_at': item.published_at.isoformat(),
                    'author_name': item.author_name,
                    'likes': item.likes,
                    'shares': item.shares,
                    'comments': item.comments,
                    'summary': item.summary
                }
                result.append(item_dict)

            return result

        except Exception as e:
            logger.error(f"Error retrieving content from database: {str(e)}")
            raise
        finally:
            db.close()

    @staticmethod
    def get_available_dates(limit=30):
        """
        Get a list of dates that have content available.

        Args:
            limit (int): Maximum number of dates to retrieve.

        Returns:
            list: List of dates in ISO format (YYYY-MM-DD).
        """
        db = next(get_db())

        try:
            # Use raw SQL that's compatible with SQL Server
            from sqlalchemy.sql import text

            # SQL Server compatible query - use string formatting for TOP clause
            sql_query = text(f"""
                SELECT TOP {limit}
                    CONVERT(DATE, published_at) as date,
                    COUNT(id) as count
                FROM content 
                GROUP BY CONVERT(DATE, published_at)
                ORDER BY CONVERT(DATE, published_at) DESC
            """)

            results = db.execute(sql_query).fetchall()

            # Convert to list of dictionaries
            dates = []
            for row in results:
                date_str = row.date.isoformat() if hasattr(row.date, 'isoformat') else str(row.date)
                dates.append({
                    'date': date_str,
                    'count': row.count
                })

            return dates

        except Exception as e:
            logger.error(f"Error retrieving available dates: {str(e)}")
            raise
        finally:
            db.close()


# Initialize database tables
def initialize_database():
    """
    Initialize the database and create default categories.
    """
    try:
        # Create tables
        init_db()

        # Create default categories
        db = next(get_db())

        # Check if categories already exist
        if db.query(Category).count() == 0:
            categories = [
                Category(name="Research", description="AI research papers and breakthroughs"),
                Category(name="Product Releases", description="New AI products and features"),
                Category(name="Opinion Pieces", description="Thought leadership and opinions on AI"),
                Category(name="Newsletters", description="AI newsletters and digests"),
                Category(name="Social Media", description="AI discussions on social media")
            ]

            db.add_all(categories)
            db.commit()
            logger.info("Default categories created")

        logger.info("Database initialized successfully")

    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise
