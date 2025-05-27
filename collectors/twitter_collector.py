"""
Twitter data collection module for the AI Dashboard.
"""
import tweepy
import json
from datetime import datetime, timedelta
import time

from src.utils.config import (
    TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, 
    TWITTER_ACCESS_SECRET, TWITTER_BEARER_TOKEN,
    TWITTER_AI_HASHTAGS, TWITTER_KEY_ACCOUNTS
)
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger('twitter_collector')

class TwitterCollector:
    """
    Collects AI-related tweets from Twitter using the Twitter API v2.
    """
    
    def __init__(self):
        """
        Initialize the Twitter collector with API credentials.
        """
        try:
            # Initialize the Twitter API client
            self.client = tweepy.Client(
                bearer_token=TWITTER_BEARER_TOKEN,
                consumer_key=TWITTER_API_KEY,
                consumer_secret=TWITTER_API_SECRET,
                access_token=TWITTER_ACCESS_TOKEN,
                access_token_secret=TWITTER_ACCESS_SECRET,
                wait_on_rate_limit=True  # Enable automatic waiting for rate limits
            )
            logger.info("Twitter API client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Twitter API client: {str(e)}")
            raise
    
    def collect_tweets_by_hashtags(self, hashtags=None, max_results=10, days_ago=1):
        """
        Collect tweets containing specific AI-related hashtags.
        
        Args:
            hashtags (list): List of hashtags to search for.
            max_results (int): Maximum number of tweets to retrieve.
            days_ago (int): How many days back to search.
            
        Returns:
            list: List of collected tweets.
        """
        if hashtags is None:
            hashtags = TWITTER_AI_HASHTAGS
            
        # Create query string from hashtags
        query = " OR ".join(hashtags)
        
        # Set time range
        end_time = datetime.utcnow() - timedelta(minutes=1)
        start_time = end_time - timedelta(days=days_ago)
        
        try:
            logger.info(f"Collecting tweets with hashtags: {hashtags}")
            
            # Search for tweets
            tweets = []
            for hashtag in hashtags:
                response = self.client.search_recent_tweets(
                    query=hashtag,
                    max_results=max_results,
                    tweet_fields=['created_at', 'public_metrics', 'author_id', 'text'],
                    user_fields=['username', 'name', 'profile_image_url'],
                    expansions=['author_id'],
                    start_time=start_time,
                    end_time=end_time
                )
                
                if response.data:
                    # Create a dictionary to map user IDs to user data
                    users = {user.id: user for user in response.includes['users']} if 'users' in response.includes else {}
                    
                    for tweet in response.data:
                        tweet_data = {
                            'id': tweet.id,
                            'text': tweet.text,
                            'created_at': tweet.created_at.isoformat(),
                            'likes': tweet.public_metrics['like_count'],
                            'retweets': tweet.public_metrics['retweet_count'],
                            'replies': tweet.public_metrics['reply_count'],
                            'source': 'twitter',
                            'hashtag': hashtag,
                            'url': f"https://twitter.com/user/status/{tweet.id}"
                        }
                        
                        # Add user information if available
                        if tweet.author_id in users:
                            user = users[tweet.author_id]
                            tweet_data['author'] = {
                                'id': user.id,
                                'username': user.username,
                                'name': user.name,
                                'profile_image_url': user.profile_image_url
                            }
                        
                        tweets.append(tweet_data)
                
                # Respect rate limits
                time.sleep(1)
            
            logger.info(f"Collected {len(tweets)} tweets with hashtags")
            return tweets
            
        except Exception as e:
            logger.error(f"Error collecting tweets by hashtags: {str(e)}")
            return []
    
    def collect_tweets_from_accounts(self, accounts=None, max_results=5, days_ago=1):
        """
        Collect tweets from specific AI-related accounts.
        
        Args:
            accounts (list): List of Twitter accounts to fetch tweets from.
            max_results (int): Maximum number of tweets to retrieve per account.
            days_ago (int): How many days back to search.
            
        Returns:
            list: List of collected tweets.
        """
        if accounts is None:
            accounts = TWITTER_KEY_ACCOUNTS
            
        tweets = []
        
        try:
            logger.info(f"Collecting tweets from accounts: {accounts}")
            
            for account in accounts:
                # Get user ID from username
                user_response = self.client.get_user(username=account)
                if not user_response.data:
                    logger.warning(f"User {account} not found")
                    continue
                    
                user_id = user_response.data.id
                
                # Get tweets from user
                response = self.client.get_users_tweets(
                    id=user_id,
                    max_results=max_results,
                    tweet_fields=['created_at', 'public_metrics', 'text'],
                    exclude=['retweets', 'replies'],
                    start_time=datetime.utcnow() - timedelta(days=days_ago)
                )
                
                if response.data:
                    for tweet in response.data:
                        tweet_data = {
                            'id': tweet.id,
                            'text': tweet.text,
                            'created_at': tweet.created_at.isoformat(),
                            'likes': tweet.public_metrics['like_count'],
                            'retweets': tweet.public_metrics['retweet_count'],
                            'replies': tweet.public_metrics['reply_count'],
                            'source': 'twitter',
                            'account': account,
                            'url': f"https://twitter.com/{account}/status/{tweet.id}",
                            'author': {
                                'id': user_id,
                                'username': account,
                                'name': user_response.data.name
                            }
                        }
                        tweets.append(tweet_data)
                
                # Respect rate limits
                time.sleep(1)
            
            logger.info(f"Collected {len(tweets)} tweets from accounts")
            return tweets
            
        except Exception as e:
            logger.error(f"Error collecting tweets from accounts: {str(e)}")
            return []
    
    def collect_all_tweets(self, max_results=10, days_ago=1):
        """
        Collect all AI-related tweets from both hashtags and key accounts.
        
        Args:
            max_results (int): Maximum number of tweets to retrieve per search.
            days_ago (int): How many days back to search.
            
        Returns:
            list: List of all collected tweets.
        """
        hashtag_tweets = self.collect_tweets_by_hashtags(max_results=max_results, days_ago=days_ago)
        account_tweets = self.collect_tweets_from_accounts(max_results=max_results, days_ago=days_ago)
        
        all_tweets = hashtag_tweets + account_tweets
        
        # Remove duplicates based on tweet ID
        unique_tweets = {tweet['id']: tweet for tweet in all_tweets}
        
        return list(unique_tweets.values())


# For testing
if __name__ == "__main__":
    collector = TwitterCollector()
    tweets = collector.collect_all_tweets(max_results=1, days_ago=1)
    
    # Save to a JSON file for inspection
    with open('twitter_data_sample.json', 'w') as f:
        json.dump(tweets, f, indent=2)
    
    print(f"Collected {len(tweets)} tweets")
