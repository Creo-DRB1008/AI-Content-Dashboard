"""
LinkedIn data collection module for the AI Dashboard.

This implementation uses third-party services (Lix or Piloterr) to access
LinkedIn content, as mentioned in the project README.
"""
import requests
import urllib.parse
from datetime import datetime, timedelta
import time
import json
import os
import sys

# Add the project root directory to the Python path
# This allows the script to be run directly
if __name__ == "__main__":
    # Get the absolute path of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the project root directory (two levels up from current file)
    project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
    # Add the project root to the Python path
    sys.path.insert(0, project_root)

# Now imports from src will work whether run as a module or directly
from src.utils.config import LINKEDIN_API_KEY
from src.utils.logger import setup_logger

# Set up logger
logger = setup_logger('linkedin_collector')

class LinkedInCollector:
    """
    Collects AI-related posts from LinkedIn using third-party services.

    This implementation works with services like Lix that provide
    access to LinkedIn content through their APIs.
    """

    def __init__(self, service_name="lix", api_key=None):
        """
        Initialize the LinkedIn collector with third-party service credentials.

        Args:
            service_name (str): Name of the third-party service ('lix')
            api_key (str): API key for the third-party service
        """
        self.service_name = service_name
        self.api_key = api_key

        # If no API key is provided, try to get it from config
        if not self.api_key:
            from src.utils.config import LINKEDIN_API_KEY
            self.api_key = LINKEDIN_API_KEY

        # Service-specific endpoints
        self.service_endpoints = {
            'lix': {
                'base_url': 'https://api.lix-it.com/v1/li',
                'search_endpoint': '/linkedin/search/posts'
            }
        }

        # Key AI companies and influencers to track
        self.key_companies = [
            'openai', 'anthropic', 'google ai', 'meta ai', 'deepmind',
            'stability ai', 'midjourney', 'microsoft ai'
        ]

        self.key_influencers = [
            'andrew ng', 'yann lecun', 'geoffrey hinton', 'fei-fei li',
            'demis hassabis', 'sam altman', 'dario amodei'
        ]

        # AI-related keywords for content filtering
        self.ai_keywords = [
            'artificial intelligence', 'machine learning', 'deep learning',
            'neural network', 'llm', 'large language model', 'gpt', 'generative ai'
        ]

        logger.info(f"LinkedIn collector initialized with {service_name} service")

    def _make_request(self, search_term):
        """
        Make a request to the Lix API using the URL-based search approach.

        Args:
            search_term (str): The search term to look for on LinkedIn

        Returns:
            dict: API response
        """
        if not self.api_key:
            logger.error("No API key provided for Lix service")
            return None

        service_config = self.service_endpoints.get(self.service_name)
        if not service_config:
            logger.error(f"Unknown service: {self.service_name}")
            return None

        # Create LinkedIn search URL
        linkedin_url = f"https://www.linkedin.com/search/results/content/?keywords={search_term}&origin=SWITCH_SEARCH_VERTICAL&sid=V2J"

        # Encode the URL
        encoded_url = urllib.parse.quote(linkedin_url, safe='')

        # Construct the full API URL
        url = f"{service_config['base_url']}{service_config['search_endpoint']}?url={encoded_url}"

        headers = {
            'Authorization': self.api_key
        }

        payload = {}

        try:
            logger.debug(f"Making request to {url}")
            response = requests.request("GET", url, headers=headers, data=payload)
            response.raise_for_status()
            response_data = response.json()
            # Log the response structure for debugging
            logger.debug(f"Response structure: {json.dumps(response_data, indent=2)[:500]}...")
            return response_data
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to {self.service_name}: {str(e)}")
            return None

    def collect_company_posts(self, company_name, max_results=10):
        """
        Collect posts related to a specific company.

        Args:
            company_name (str): Company name to search for
            max_results (int): Maximum number of posts to retrieve

        Returns:
            list: List of collected posts
        """
        return self.collect_posts_by_keyword(company_name, max_results)

    def collect_influencer_posts(self, influencer_name, max_results=10):
        """
        Collect posts from a specific influencer.

        Args:
            influencer_name (str): Influencer name to search for
            max_results (int): Maximum number of posts to retrieve

        Returns:
            list: List of collected posts
        """
        return self.collect_posts_by_keyword(influencer_name, max_results)

    def collect_posts_by_keyword(self, keyword, max_results=10):
        """
        Collect LinkedIn posts related to a specific keyword.

        Args:
            keyword (str): Keyword to search for
            max_results (int): Maximum number of posts to retrieve

        Returns:
            list: List of collected posts
        """
        logger.info(f"Collecting LinkedIn posts for keyword: {keyword}")

        if not self.api_key:
            logger.error("No API key provided for Lix service. Cannot collect real data.")
            return []

        response = self._make_request(keyword)
        if not response:
            logger.warning(f"No response from Lix for keyword {keyword}")
            return []

        # Process and format the response
        posts = self._process_posts(response)

        # Limit the number of posts if needed
        if max_results and len(posts) > max_results:
            posts = posts[:max_results]

        logger.info(f"Collected {len(posts)} posts for keyword {keyword}")
        return posts

    def _process_posts(self, response):
        """
        Process and format posts from Lix API response.

        Args:
            response (dict): API response

        Returns:
            list: Formatted posts
        """
        formatted_posts = []

        # Check if the response contains posts in the new format
        if 'posts' in response and isinstance(response['posts'], list):
            posts = response['posts']

            for post in posts:
                # Extract post ID
                post_id = post.get('id', f"lix-{len(formatted_posts)}")

                # Extract post content
                text = post.get('text', '')
                if not text and 'embeddedObject' in post:
                    # Try to get text from embedded object title
                    text = post.get('embeddedObject', {}).get('title', '')

                # Extract author information
                author = {}
                if 'actor' in post:
                    actor = post.get('actor', {})
                    author = {
                        'id': actor.get('id', ''),
                        'name': actor.get('name', ''),
                        'profile_url': actor.get('url', '')
                    }

                # Extract engagement metrics
                likes = 0
                comments = 0
                shares = 0

                # Try to get reaction counts
                if 'numReactions' in post:
                    for reaction in post.get('numReactions', []):
                        if reaction.get('reactionType') == 'REACTION_TYPE_LIKE':
                            likes += reaction.get('count', 0)
                        # Add other reaction types if needed

                # Try to get comment count
                comments = post.get('commentCount', 0)

                # Create formatted post
                formatted_post = {
                    'id': post_id,
                    'text': text,
                    'created_at': post.get('createdAt', datetime.utcnow().isoformat()),
                    'likes': likes,
                    'comments': comments,
                    'shares': shares,
                    'source': 'linkedin',
                    'url': post.get('url', ''),
                    'author': author
                }

                formatted_posts.append(formatted_post)

        # Fallback to old format if new format not found
        elif 'data' in response and 'elements' in response['data']:
            elements = response['data']['elements']

            for element in elements:
                # Skip non-post elements
                if 'post' not in element:
                    continue

                post_data = element['post']

                # Extract author information
                author = {}
                if 'author' in post_data:
                    author = {
                        'id': post_data['author'].get('urn', ''),
                        'name': post_data['author'].get('name', ''),
                        'profile_url': post_data['author'].get('navigationUrl', '')
                    }

                # Extract post content
                text = ''
                if 'commentary' in post_data:
                    text = post_data['commentary'].get('text', '')

                # Extract engagement metrics
                likes = 0
                comments = 0
                shares = 0
                if 'socialDetail' in post_data:
                    social = post_data['socialDetail']
                    likes = social.get('totalReactions', 0)
                    comments = social.get('comments', 0)
                    shares = social.get('totalShares', 0)

                # Create formatted post
                post = {
                    'id': post_data.get('urn', f"lix-{len(formatted_posts)}"),
                    'text': text,
                    'created_at': post_data.get('postedAt', datetime.utcnow().isoformat()),
                    'likes': likes,
                    'comments': comments,
                    'shares': shares,
                    'source': 'linkedin',
                    'url': post_data.get('navigationUrl', ''),
                    'author': author
                }

                formatted_posts.append(post)

        return formatted_posts

    def collect_all_posts(self, max_results=10):
        """
        Collect all AI-related posts from both companies and influencers.

        Args:
            max_results (int): Maximum number of posts to retrieve per entity

        Returns:
            list: List of all collected posts
        """
        all_posts = []

        if not self.api_key:
            logger.error("No API key provided. Cannot collect real LinkedIn data.")
            return []

        # Collect posts from companies
        for company in self.key_companies:
            try:
                company_posts = self.collect_company_posts(company, max_results)
                all_posts.extend(company_posts)
                # Add delay to avoid rate limiting
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error collecting posts from company {company}: {str(e)}")

        # Collect posts from influencers
        for influencer in self.key_influencers:
            try:
                influencer_posts = self.collect_influencer_posts(influencer, max_results)
                all_posts.extend(influencer_posts)
                # Add delay to avoid rate limiting
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error collecting posts from influencer {influencer}: {str(e)}")

        # Collect posts for AI keywords
        for keyword in self.ai_keywords:
            try:
                keyword_posts = self.collect_posts_by_keyword(keyword, max_results)
                all_posts.extend(keyword_posts)
                # Add delay to avoid rate limiting
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error collecting posts for keyword {keyword}: {str(e)}")

        # Remove duplicate posts
        unique_posts = []
        seen_ids = set()
        for post in all_posts:
            if post['id'] not in seen_ids:
                seen_ids.add(post['id'])
                unique_posts.append(post)

        logger.info(f"Collected {len(unique_posts)} unique LinkedIn posts")
        return unique_posts

    def _simulate_company_posts(self, company_id, count=5, days_ago=7):
        """Generate simulated company posts for testing"""
        posts = []
        company_name = company_id.replace('-', ' ').title()

        for i in range(count):
            post = {
                'id': f"{company_id}-post-{i}",
                'text': f"Simulated LinkedIn post from {company_name} about our latest AI developments.",
                'created_at': (datetime.utcnow() - timedelta(days=i % days_ago)).isoformat(),
                'likes': 100 + i * 10,
                'comments': 20 + i * 2,
                'shares': 5 + i,
                'source': 'linkedin',
                'company': company_name,
                'url': f"https://linkedin.com/company/{company_id}/posts/simulated-{i}",
                'author': {
                    'id': f"company-{company_id}",
                    'name': company_name,
                    'profile_url': f"https://linkedin.com/company/{company_id}"
                }
            }
            posts.append(post)

        return posts

    def _simulate_influencer_posts(self, influencer_id, count=5, days_ago=7):
        """Generate simulated influencer posts for testing"""
        posts = []
        influencer_name = influencer_id.replace('-', ' ').title()

        for i in range(count):
            post = {
                'id': f"{influencer_id}-post-{i}",
                'text': f"Simulated LinkedIn post from {influencer_name} sharing thoughts on recent AI advancements.",
                'created_at': (datetime.utcnow() - timedelta(days=i % days_ago)).isoformat(),
                'likes': 200 + i * 15,
                'comments': 30 + i * 3,
                'shares': 10 + i * 2,
                'source': 'linkedin',
                'url': f"https://linkedin.com/in/{influencer_id}/posts/simulated-{i}",
                'author': {
                    'id': influencer_id,
                    'name': influencer_name,
                    'profile_url': f"https://linkedin.com/in/{influencer_id}"
                }
            }
            posts.append(post)

        return posts

    def simulate_data(self, count=5):
        """
        Generate simulated LinkedIn data for testing purposes.

        Args:
            count (int): Number of simulated posts to generate.

        Returns:
            list: List of simulated LinkedIn posts.
        """
        logger.info(f"Generating {count} simulated LinkedIn posts")

        simulated_posts = []
        companies = ['OpenAI', 'Google AI', 'Anthropic', 'DeepMind', 'Meta AI']

        for i in range(count):
            company_index = i % len(companies)
            days_ago = i % 7

            post = {
                'id': f"simulated-linkedin-{i}",
                'text': f"Simulated LinkedIn post about AI from {companies[company_index]}. This is test data for development purposes.",
                'created_at': (datetime.utcnow() - timedelta(days=days_ago)).isoformat(),
                'likes': 100 + i * 10,
                'comments': 20 + i * 2,
                'shares': 5 + i,
                'source': 'linkedin',
                'company': companies[company_index],
                'url': f"https://linkedin.com/company/{companies[company_index].lower().replace(' ', '-')}/posts/simulated-{i}",
                'author': {
                    'id': f"company-{company_index}",
                    'name': companies[company_index],
                    'profile_url': f"https://linkedin.com/company/{companies[company_index].lower().replace(' ', '-')}"
                }
            }

            simulated_posts.append(post)

        return simulated_posts


# For testing
if __name__ == "__main__":
    # Import API key from environment if available
    import os
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # Get API key from environment
    api_key = os.getenv('LINKEDIN_API_KEY')

    # Initialize collector with API key
    collector = LinkedInCollector(service_name="lix", api_key=api_key)

    # Test if we have a valid API key
    if collector.api_key:
        print(f"Using API key: {collector.api_key[:5]}...")

        try:
            # Test keyword search
            print("\nTesting keyword search...")
            keyword_posts = collector.collect_posts_by_keyword("artificial intelligence", max_results=3)
            print(f"Collected {len(keyword_posts)} posts for 'artificial intelligence'")

            # Print first post if available
            if keyword_posts:
                print(f"Sample post: {keyword_posts[0]['text'][:100]}...")

            # Test company posts collection
            print("\nTesting company posts collection...")
            company_posts = collector.collect_company_posts("openai", max_results=3)
            print(f"Collected {len(company_posts)} posts for OpenAI")

            # Print first post if available
            if company_posts:
                print(f"Sample post: {company_posts[0]['text'][:100]}...")

            # Test influencer posts collection
            print("\nTesting influencer posts collection...")
            influencer_posts = collector.collect_influencer_posts("sam altman", max_results=3)
            print(f"Collected {len(influencer_posts)} posts for Sam Altman")

            # Print first post if available
            if influencer_posts:
                print(f"Sample post: {influencer_posts[0]['text'][:100]}...")

            # Save results to file for inspection
            with open("data/data/twitter_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
                json.dump({
                    'keyword_posts': keyword_posts,
                    'company_posts': company_posts,
                    'influencer_posts': influencer_posts
                }, f, indent=2)

            print("\nResults saved to linkedin_real_data_test.json")
        except Exception as e:
            print(f"Error testing real data collection: {str(e)}")
            print("Check your API key and service endpoints.")
    else:
        print("No API key available. Cannot test real data collection.")
        print("Please set LINKEDIN_API_KEY in your .env file.")

        # Use simulated data as fallback
        print("\nFalling back to simulated data for testing...")
        simulated_posts = collector.simulate_data(5)
        print(f"Generated {len(simulated_posts)} simulated posts")

        # Save simulated data
        with open('linkedin_simulated_data.json', 'w') as f:
            json.dump(simulated_posts, f, indent=2)

        print("Simulated data saved to linkedin_simulated_data.json")
