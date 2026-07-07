"""
Fetch news articles from NewsAPI
"""
import logging
import requests
from typing import List, Dict
from config import NEWS_API_KEY, NEWS_API_URL, NEWS_KEYWORDS

logger = logging.getLogger(__name__)


class NewsFetcher:
    """Fetch trending news articles from multiple sources"""
    
    def __init__(self):
        self.api_key = NEWS_API_KEY
        self.api_url = NEWS_API_URL
        self.headers = {"Authorization": self.api_key}
    
    def fetch_top_headlines(self, category: str = "general", limit: int = 5) -> List[Dict]:
        """
        Fetch top headlines from NewsAPI
        
        Args:
            category: news category (general, business, technology, etc.)
            limit: number of articles to fetch
            
        Returns:
            List of article dictionaries with title, description, url, source, image, etc.
        """
        try:
            endpoint = f"{self.api_url}/top-headlines"
            params = {
                "category": category,
                "language": "en",
                "pageSize": limit,
                "apiKey": self.api_key
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") != "ok":
                logger.error(f"API error: {data.get('message')}")
                return []
            
            articles = data.get("articles", [])
            logger.info(f"Fetched {len(articles)} articles from category: {category}")
            
            return self._clean_articles(articles)
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch news: {e}")
            return []
    
    def fetch_by_keywords(self, keywords: List[str], limit: int = 5) -> List[Dict]:
        """
        Fetch articles by search keywords
        
        Args:
            keywords: list of search terms
            limit: number of articles per keyword
            
        Returns:
            List of article dictionaries
        """
        all_articles = []
        
        for keyword in keywords:
            try:
                endpoint = f"{self.api_url}/everything"
                params = {
                    "q": keyword,
                    "language": "en",
                    "sortBy": "publishedAt",
                    "pageSize": limit,
                    "apiKey": self.api_key
                }
                
                response = requests.get(endpoint, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                if data.get("status") == "ok":
                    articles = data.get("articles", [])
                    all_articles.extend(articles)
                    logger.info(f"Fetched {len(articles)} articles for keyword: {keyword}")
            
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to fetch news for keyword '{keyword}': {e}")
        
        return self._clean_articles(all_articles)
    
    def _clean_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Clean and validate articles
        
        Args:
            articles: raw articles from API
            
        Returns:
            Cleaned articles with required fields
        """
        cleaned = []
        
        for article in articles:
            # Skip articles with missing critical fields
            if not article.get("title") or not article.get("description"):
                continue
            
            # Skip articles from certain sources
            if article.get("source", {}).get("name", "").lower() in ["removed"]:
                continue
            
            cleaned_article = {
                "id": article.get("url"),  # Use URL as unique ID
                "title": article.get("title", "").strip(),
                "description": article.get("description", "").strip(),
                "content": article.get("content", "").strip(),
                "url": article.get("url"),
                "source": article.get("source", {}).get("name", "Unknown"),
                "published_at": article.get("publishedAt"),
                "image": article.get("urlToImage"),
            }
            
            cleaned.append(cleaned_article)
        
        return cleaned
    
    def get_trending_stories(self, limit: int = 5) -> List[Dict]:
        """
        Get trending stories across multiple categories
        
        Args:
            limit: number of stories per category
            
        Returns:
            List of trending articles
        """
        categories = ["technology", "business", "health", "science"]
        trending = []
        
        for category in categories:
            articles = self.fetch_top_headlines(category=category, limit=limit)
            trending.extend(articles)
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_articles = []
        
        for article in trending:
            if article.get("url") not in seen_urls:
                unique_articles.append(article)
                seen_urls.add(article.get("url"))
        
        return unique_articles[:limit]


if __name__ == "__main__":
    # Test the fetcher
    logging.basicConfig(level=logging.INFO)
    
    fetcher = NewsFetcher()
    articles = fetcher.fetch_top_headlines(category="technology", limit=3)
    
    for article in articles:
        print(f"\nTitle: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"Description: {article['description'][:100]}...")
