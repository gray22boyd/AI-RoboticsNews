#!/usr/bin/env python3
"""
RSS News Monitor
Fetches AI & robotics news from free RSS feeds (no paywalls)
Better alternative to NewsAPI for accessible content
"""

import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import time
import feedparser
from urllib.parse import urljoin, urlparse
import re
from config import FREE_RSS_FEEDS, NEWS_ARTICLES_LIMIT
from utils import rate_limit, safe_request, truncate_text

logger = logging.getLogger(__name__)

class RSSNewsMonitor:
    def __init__(self):
        self.ai_robotics_headlines = []
        self.processed_articles = []
    
    def fetch_rss_feed(self, feed_config: Dict[str, str]) -> List[Dict[str, Any]]:
        """Fetch and parse RSS feed from a source"""
        try:
            logger.info(f"Fetching RSS feed: {feed_config['name']}")
            
            # Fetch the RSS feed
            response = requests.get(feed_config['url'], timeout=10)
            response.raise_for_status()
            
            # Parse RSS content
            feed = feedparser.parse(response.content)
            
            if not feed.entries:
                logger.warning(f"No entries found in feed: {feed_config['name']}")
                return []
            
            articles = []
            for entry in feed.entries[:5]:  # Get top 5 from each feed
                article = self._process_rss_entry(entry, feed_config)
                if article and self._is_relevant_article(article):
                    articles.append(article)
            
            logger.info(f"Found {len(articles)} relevant articles from {feed_config['name']}")
            return articles
        
        except Exception as e:
            logger.error(f"Error fetching RSS feed {feed_config['name']}: {e}")
            return []
    
    def _process_rss_entry(self, entry: Any, feed_config: Dict[str, str]) -> Dict[str, Any]:
        """Process individual RSS entry into article format"""
        try:
            # Extract basic information
            title = getattr(entry, 'title', '').strip()
            description = getattr(entry, 'summary', '') or getattr(entry, 'description', '')
            description = self._clean_html(description).strip()
            
            # Skip articles with insufficient content
            if not title or len(title) < 10:
                return None
            
            # Get publication date
            published_at = ''
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    pub_date = datetime(*entry.published_parsed[:6])
                    published_at = pub_date.strftime('%Y-%m-%d %H:%M')
                except:
                    published_at = getattr(entry, 'published', '')
            else:
                published_at = getattr(entry, 'published', '')
            
            # Get URL
            url = getattr(entry, 'link', '')
            
            # Calculate relevance score
            relevance_score = self._calculate_relevance_score(title, description)
            
            # Skip articles that are too old (older than 7 days)
            if not self._is_recent_article(published_at):
                return None
            
            article_data = {
                'title': title,
                'description': truncate_text(description, 400),
                'url': url,
                'source': feed_config['name'],
                'source_category': feed_config['category'],
                'published_at': published_at,
                'relevance_score': relevance_score,
                'is_headline': self._is_ai_robotics_headline(title, description),
                'content_preview': truncate_text(description, 200),
                'keyword': self._extract_main_keyword(title, description)
            }
            
            return article_data
        
        except Exception as e:
            logger.error(f"Error processing RSS entry: {e}")
            return None
    
    def _clean_html(self, text: str) -> str:
        """Remove HTML tags and clean text"""
        if not text:
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Decode HTML entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        
        return text.strip()
    
    def _is_recent_article(self, published_at: str) -> bool:
        """Check if article is recent (within last 7 days)"""
        if not published_at:
            return True  # If no date, assume recent
        
        try:
            if isinstance(published_at, str):
                # Try to parse various date formats
                for fmt in ['%Y-%m-%d %H:%M', '%Y-%m-%d', '%a, %d %b %Y %H:%M:%S']:
                    try:
                        pub_date = datetime.strptime(published_at[:19], fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return True  # If can't parse, assume recent
            
            # Check if within last 7 days
            cutoff_date = datetime.now() - timedelta(days=7)
            return pub_date >= cutoff_date
        
        except:
            return True  # If error, assume recent
    
    def _is_relevant_article(self, article: Dict) -> bool:
        """Check if article is relevant to AI/robotics"""
        title_lower = article.get('title', '').lower()
        desc_lower = article.get('description', '').lower()
        
        # AI/robotics keywords
        ai_keywords = [
            'artificial intelligence', 'ai', 'machine learning', 'deep learning',
            'neural network', 'robotics', 'robot', 'automation', 'autonomous',
            'chatgpt', 'gpt', 'llm', 'language model', 'computer vision',
            'nlp', 'natural language', 'reinforcement learning', 'transformer',
            'openai', 'deepmind', 'anthropic', 'claude', 'gemini', 'tesla',
            'nvidia', 'boston dynamics', 'figure', 'sanctuary', 'humanoid'
        ]
        
        full_text = f"{title_lower} {desc_lower}"
        
        # Must contain at least one AI/robotics keyword
        if not any(keyword in full_text for keyword in ai_keywords):
            return False
        
        # Filter out irrelevant content
        irrelevant_terms = [
            'cryptocurrency', 'crypto', 'blockchain', 'nft', 'bitcoin',
            'stock price', 'market cap', 'dividend', 'earnings call'
        ]
        
        if any(term in full_text for term in irrelevant_terms):
            return False
        
        return True
    
    def _calculate_relevance_score(self, title: str, description: str) -> float:
        """Calculate relevance score for article"""
        score = 0.0
        
        title_lower = title.lower()
        desc_lower = description.lower()
        full_text = f"{title_lower} {desc_lower}"
        
        # High-value keywords (company/product names)
        high_value_terms = [
            'openai', 'chatgpt', 'gpt-4', 'deepmind', 'anthropic', 'claude',
            'google ai', 'microsoft ai', 'nvidia', 'tesla', 'figure ai',
            'boston dynamics', 'sanctuary ai', 'humanoid robot'
        ]
        
        for term in high_value_terms:
            if term in full_text:
                score += 2.0
        
        # Medium-value keywords
        medium_value_terms = [
            'artificial intelligence', 'machine learning', 'deep learning',
            'neural network', 'robotics', 'automation', 'computer vision'
        ]
        
        for term in medium_value_terms:
            if term in full_text:
                score += 1.0
        
        # Title bonus
        if any(term in title_lower for term in high_value_terms + medium_value_terms):
            score += 1.0
        
        return min(score, 5.0)  # Cap at 5.0
    
    def _is_ai_robotics_headline(self, title: str, description: str) -> bool:
        """Check if this is a major AI/robotics headline"""
        full_text = f"{title.lower()} {description.lower()}"
        
        headline_indicators = [
            'announces', 'launches', 'releases', 'unveils', 'introduces',
            'breakthrough', 'new model', 'partnership', 'acquisition',
            'funding', 'milestone', 'first time', 'revolutionary',
            'open source', 'research', 'study finds'
        ]
        
        return any(indicator in full_text for indicator in headline_indicators)
    
    def _extract_main_keyword(self, title: str, description: str) -> str:
        """Extract main keyword/topic from article"""
        full_text = f"{title} {description}".lower()
        
        # Priority keywords mapping
        keyword_map = {
            'openai': 'OpenAI',
            'chatgpt': 'ChatGPT',
            'deepmind': 'DeepMind',
            'anthropic': 'Anthropic',
            'claude': 'Claude',
            'gemini': 'Gemini',
            'tesla': 'Tesla',
            'nvidia': 'NVIDIA',
            'microsoft': 'Microsoft',
            'google': 'Google',
            'boston dynamics': 'Boston Dynamics',
            'figure ai': 'Figure AI',
            'sanctuary ai': 'Sanctuary AI',
            'humanoid': 'Humanoid Robotics',
            'robotics': 'Robotics',
            'machine learning': 'Machine Learning',
            'artificial intelligence': 'AI'
        }
        
        for keyword, display_name in keyword_map.items():
            if keyword in full_text:
                return display_name
        
        return 'AI'
    
    def monitor_all_feeds(self) -> List[Dict[str, Any]]:
        """Monitor all configured RSS feeds"""
        all_articles = []
        feed_stats = {}
        
        logger.info("Starting RSS news monitoring from free sources...")
        
        for feed_config in FREE_RSS_FEEDS:
            try:
                articles = self.fetch_rss_feed(feed_config)
                feed_stats[feed_config['name']] = len(articles)
                all_articles.extend(articles)
                
                # Respectful delay between requests
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Failed to fetch RSS feed '{feed_config['name']}': {e}")
                feed_stats[feed_config['name']] = 0
                continue
        
        # Log feed statistics
        logger.info("RSS feed results:")
        for feed_name, count in feed_stats.items():
            logger.info(f"  {feed_name}: {count} articles")
        
        # Remove duplicates
        unique_articles = self._remove_duplicates(all_articles)
        
        # Identify headline stories
        headlines = [a for a in unique_articles if a.get('is_headline', False)]
        self.ai_robotics_headlines = headlines[:5]
        
        # Sort by relevance and recency
        unique_articles.sort(key=lambda x: (x['relevance_score'], x.get('published_at', '')), reverse=True)
        
        logger.info(f"Found {len(headlines)} AI/robotics headlines")
        logger.info(f"RSS monitoring complete. Found {len(unique_articles)} unique articles")
        
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
    monitor = RSSNewsMonitor()
    articles = monitor.monitor_all_feeds()
    print(f"✅ Found {len(articles)} free, accessible articles")
    
    headlines = monitor.get_top_headlines()
    print(f"📈 Top headlines: {len(headlines)}")
    
    for i, headline in enumerate(headlines[:3], 1):
        print(f"{i}. {headline['title']}")
        print(f"   Source: {headline['source']} | Score: {headline['relevance_score']:.1f}")
        print(f"   URL: {headline['url']}")
        print() 