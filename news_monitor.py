#!/usr/bin/env python3
"""
Enhanced News Monitor
Fetches AI & robotics news with improved keyword coverage and duplicate filtering
"""

import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import time
from config import NEWS_API_KEY, NEWS_KEYWORDS, NEWS_ARTICLES_LIMIT
from utils import rate_limit, safe_request, get_yesterday_date, truncate_text

logger = logging.getLogger(__name__)

class NewsMonitor:
    def __init__(self):
        self.api_key = NEWS_API_KEY
        self.base_url = 'https://newsapi.org/v2/everything'
        self.ai_robotics_headlines = []
    
    @rate_limit(calls_per_minute=100)  # NewsAPI allows 1000 calls per day
    def search_news(self, keyword: str, max_articles: int = 10) -> List[Dict[str, Any]]:
        """Search for news articles using NewsAPI"""
        
        # Get date range (last 3 days for better coverage)
        from_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
        
        params = {
            'q': f'"{keyword}"',  # Use exact phrase matching
            'apiKey': self.api_key,
            'language': 'en',
            'sortBy': 'relevancy',
            'from': from_date,
            'pageSize': max_articles * 2  # Get extra to filter later
        }
        
        try:
            logger.info(f"Searching news for keyword: {keyword}")
            response = safe_request(self.base_url, params=params)
            
            if response.status_code != 200:
                logger.error(f"NewsAPI returned status {response.status_code} for keyword: {keyword}")
                return []
            
            data = response.json()
            articles = data.get('articles', [])
            
            # Process and filter articles
            processed_articles = []
            for article in articles:
                processed_article = self._process_article(article, keyword)
                if processed_article and self._is_relevant_article(processed_article, keyword):
                    processed_articles.append(processed_article)
                    if len(processed_articles) >= max_articles:
                        break
            
            logger.info(f"Found {len(processed_articles)} relevant articles for keyword: {keyword}")
            return processed_articles
            
        except Exception as e:
            logger.error(f"Error searching news for keyword '{keyword}': {e}")
            return []
    
    def _process_article(self, article: Dict, keyword: str) -> Dict[str, Any]:
        """Process and clean article data"""
        
        # Extract and clean basic information
        title = (article.get('title') or '').strip()
        description = (article.get('description') or '').strip()
        content = (article.get('content') or '').strip()
        
        # Skip articles with insufficient content
        if not title or len(title) < 10:
            return None
        
        # Clean and validate source
        source_info = article.get('source', {})
        source_name = ''
        if isinstance(source_info, dict):
            source_name = (source_info.get('name') or '').strip()
        else:
            source_name = str(source_info).strip()
        
        if not source_name:
            source_name = 'Unknown Source'
        
        # Parse publication date
        published_at = article.get('publishedAt', '')
        if published_at:
            try:
                pub_datetime = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                published_at = pub_datetime.strftime('%Y-%m-%d %H:%M')
            except:
                published_at = published_at[:19] if len(published_at) >= 19 else published_at
        
        # Calculate relevance score
        relevance_score = self._calculate_relevance_score(title, description, keyword)
        
        # Check if it's a headline story
        is_headline = self._is_ai_robotics_headline(title, description)
        
        article_data = {
            'title': title,
            'description': description[:400] + '...' if len(description) > 400 else description,
            'url': article.get('url', ''),
            'source': source_name,
            'published_at': published_at,
            'keyword': keyword,
            'relevance_score': relevance_score,
            'is_headline': is_headline,
            'content_preview': truncate_text(content, 200)
        }
        
        return article_data
    
    def _is_relevant_article(self, article: Dict, keyword: str) -> bool:
        """Check if article is relevant to AI/robotics"""
        
        # Skip articles with very low relevance
        if article.get('relevance_score', 0) < 0.3:
            return False
        
        # Skip articles that are clearly not AI/robotics related
        title_lower = article.get('title', '').lower()
        desc_lower = article.get('description', '').lower()
        
        # Filter out common false positives
        irrelevant_terms = [
            'stock price', 'market cap', 'earnings report', 'financial results',
            'share price', 'quarterly report', 'investor', 'dividend',
            'stock market', 'trading', 'wall street'
        ]
        
        full_text = f"{title_lower} {desc_lower}"
        if any(term in full_text for term in irrelevant_terms):
            # Allow if it's clearly about AI/robotics technology
            ai_tech_terms = ['artificial intelligence', 'machine learning', 'robotics', 'automation', 'ai technology']
            if not any(term in full_text for term in ai_tech_terms):
                return False
        
        return True
    
    def _calculate_relevance_score(self, title: str, description: str, keyword: str) -> float:
        """Calculate relevance score for article"""
        score = 0.0
        
        title_lower = title.lower()
        desc_lower = description.lower()
        keyword_lower = keyword.lower()
        
        # Keyword in title (highest weight)
        if keyword_lower in title_lower:
            score += 2.0
        
        # Keyword in description
        if keyword_lower in desc_lower:
            score += 1.0
        
        # AI/robotics related terms
        ai_terms = [
            'artificial intelligence', 'machine learning', 'deep learning',
            'neural network', 'robotics', 'automation', 'autonomous',
            'ai model', 'chatgpt', 'llm', 'language model', 'computer vision',
            'natural language processing', 'reinforcement learning'
        ]
        
        full_text = f"{title_lower} {desc_lower}"
        ai_term_count = sum(1 for term in ai_terms if term in full_text)
        score += min(ai_term_count * 0.3, 1.5)
        
        # Company/organization mentions
        important_orgs = [
            'openai', 'deepmind', 'anthropic', 'google', 'meta', 'microsoft',
            'tesla', 'nvidia', 'boston dynamics', 'figure', 'sanctuary ai'
        ]
        
        org_mentions = sum(1 for org in important_orgs if org in full_text)
        score += min(org_mentions * 0.4, 1.0)
        
        return score
    
    def _is_ai_robotics_headline(self, title: str, description: str) -> bool:
        """Check if this is a major AI/robotics headline"""
        
        full_text = f"{title.lower()} {description.lower()}"
        
        headline_indicators = [
            'breakthrough', 'announcement', 'launches', 'releases', 'unveils',
            'introduces', 'new model', 'partnership', 'acquisition', 'funding',
            'milestone', 'achievement', 'record', 'first time', 'revolutionary'
        ]
        
        return any(indicator in full_text for indicator in headline_indicators)
    
    def monitor_all_keywords(self) -> List[Dict[str, Any]]:
        """Monitor all configured news keywords"""
        all_articles = []
        keyword_stats = {}
        
        logger.info("Starting enhanced news monitoring...")
        
        for keyword in NEWS_KEYWORDS:
            try:
                articles = self.search_news(keyword, max_articles=8)
                keyword_stats[keyword] = len(articles)
                all_articles.extend(articles)
                
                # Respectful delay between requests
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Failed to search for keyword '{keyword}': {e}")
                keyword_stats[keyword] = 0
                continue
        
        # Log keyword statistics
        logger.info("Keyword search results:")
        for keyword, count in keyword_stats.items():
            logger.info(f"  {keyword}: {count} articles")
        
        # Remove duplicates more intelligently
        unique_articles = self._remove_duplicates(all_articles)
        
        # Identify headline stories
        headlines = [a for a in unique_articles if a.get('is_headline', False)]
        self.ai_robotics_headlines = headlines[:5]  # Top 5 headlines
        
        # Sort by relevance and recency
        unique_articles.sort(key=lambda x: (x['relevance_score'], x.get('published_at', '')), reverse=True)
        
        logger.info(f"Found {len(headlines)} AI/robotics headlines")
        logger.info(f"News monitoring complete. Found {len(unique_articles)} unique articles")
        
        return unique_articles[:NEWS_ARTICLES_LIMIT]
    
    def _remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles using intelligent matching"""
        unique_articles = []
        seen_titles = set()
        seen_urls = set()
        
        for article in articles:
            # Check for exact title duplicates
            title_key = article['title'].lower().strip()
            url_key = article.get('url', '').lower().strip()
            
            # Skip if we've seen this exact title or URL
            if title_key in seen_titles or (url_key and url_key in seen_urls):
                continue
            
            # Check for similar titles (first 50 characters)
            title_prefix = title_key[:50]
            is_similar = any(title_prefix in seen_title for seen_title in seen_titles)
            
            if not is_similar:
                seen_titles.add(title_key)
                if url_key:
                    seen_urls.add(url_key)
                unique_articles.append(article)
        
        logger.info(f"Removed {len(articles) - len(unique_articles)} duplicate articles")
        return unique_articles
    
    def get_top_headlines(self) -> List[Dict[str, Any]]:
        """Get the top AI/robotics headlines from the latest monitoring"""
        return self.ai_robotics_headlines

if __name__ == "__main__":
    monitor = NewsMonitor()
    articles = monitor.monitor_all_keywords()
    print(f"Found {len(articles)} articles")
    headlines = monitor.get_top_headlines()
    print(f"Top headlines: {len(headlines)}")
    for headline in headlines[:3]:
        print(f"- {headline['title']}")
        print(f"  Source: {headline['source']} | Relevance: {headline['relevance_score']:.1f}")
        print() 