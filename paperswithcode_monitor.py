#!/usr/bin/env python3
"""
Papers With Code Monitor
Fetches recent AI and robotics research papers from Papers With Code API
"""

import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import time
from config import PAPERSWITHCODE_KEYWORDS, PAPERS_PER_TOPIC
from utils import rate_limit, safe_request

logger = logging.getLogger(__name__)

class PapersWithCodeMonitor:
    def __init__(self):
        self.base_url = 'https://paperswithcode.com/api/v1/papers'
    
    @rate_limit(calls_per_minute=30)  # Conservative rate limiting
    def search_papers(self, query: str, max_results: int = PAPERS_PER_TOPIC) -> List[Dict[str, Any]]:
        """Search for papers using Papers With Code API"""
        
        params = {
            'q': query,
            'ordering': '-published'  # Most recent first
        }
        
        try:
            logger.info(f"Searching Papers With Code for: {query}")
            response = safe_request(self.base_url, params=params)
            
            if response.status_code != 200:
                logger.error(f"API returned status {response.status_code} for query: {query}")
                return []
            
            data = response.json()
            results = data.get('results', [])
            
            # Parse and filter papers
            papers = []
            for paper_data in results[:max_results * 2]:  # Get extra to filter
                parsed_paper = self._parse_paper_data(paper_data, query)
                if parsed_paper and self._is_recent_and_relevant(parsed_paper, query):
                    papers.append(parsed_paper)
                    if len(papers) >= max_results:
                        break
            
            logger.info(f"Found {len(papers)} relevant papers for query: {query}")
            return papers
            
        except Exception as e:
            logger.error(f"Error searching Papers With Code for query '{query}': {e}")
            return []
    
    def _parse_paper_data(self, paper_data: Dict, query: str) -> Dict[str, Any]:
        """Parse paper data from Papers With Code API response"""
        
        try:
            # Extract basic information
            title = paper_data.get('title', '').strip()
            abstract = paper_data.get('abstract', '').strip()
            
            # Skip if no meaningful content
            if not title or len(title) < 10:
                return None
            
            # Extract URL
            paper_url = paper_data.get('url_abs', '')
            if paper_url and not paper_url.startswith('http'):
                paper_url = f"https://paperswithcode.com{paper_url}"
            
            # Extract publication date
            published_date = paper_data.get('published', '')
            if published_date:
                try:
                    # Convert to standard date format
                    pub_datetime = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                    published_date = pub_datetime.strftime('%Y-%m-%d')
                except:
                    published_date = published_date[:10] if len(published_date) >= 10 else ''
            
            # Extract tasks (what the paper addresses)
            tasks = []
            if 'tasks' in paper_data and paper_data['tasks']:
                for task in paper_data['tasks'][:3]:  # Limit to top 3 tasks
                    if isinstance(task, dict):
                        tasks.append(task.get('name', ''))
                    else:
                        tasks.append(str(task))
            
            # Extract methods (techniques used)
            methods = []
            if 'methods' in paper_data and paper_data['methods']:
                for method in paper_data['methods'][:3]:  # Limit to top 3 methods
                    if isinstance(method, dict):
                        methods.append(method.get('name', ''))
                    else:
                        methods.append(str(method))
            
            # Extract repository information
            repository = ''
            if 'proceeding' in paper_data and paper_data['proceeding']:
                repo_info = paper_data['proceeding']
                if isinstance(repo_info, dict):
                    repository = repo_info.get('url', '')
            
            # Check for GitHub repository in the paper data
            if not repository and 'url_pdf' in paper_data:
                pdf_url = paper_data['url_pdf']
                if 'github.com' in str(pdf_url).lower():
                    repository = pdf_url
            
            # Calculate relevance score
            relevance_score = self._calculate_relevance(title, abstract, tasks, methods, query)
            
            # Check if from a top organization
            has_top_org = self._check_top_organization(title, abstract)
            
            # Classify paper type for clustering
            paper_type = self._classify_paper_type(title, abstract, tasks, methods)
            
            paper_info = {
                'title': title,
                'abstract': abstract[:500] + '...' if len(abstract) > 500 else abstract,
                'url': paper_url,
                'published': published_date,
                'tasks': [t for t in tasks if t],  # Remove empty strings
                'methods': [m for m in methods if m],  # Remove empty strings
                'repository': repository,
                'query': query,
                'relevance_score': relevance_score,
                'has_top_org': has_top_org,
                'paper_type': paper_type
            }
            
            return paper_info
            
        except Exception as e:
            logger.warning(f"Error parsing paper data: {e}")
            return None
    
    def _is_recent_and_relevant(self, paper: Dict, query: str) -> bool:
        """Check if paper is recent and relevant with higher quality threshold"""
        
        # Check publication date (last 6 months for broader coverage)
        if paper.get('published'):
            try:
                pub_date = datetime.strptime(paper['published'], '%Y-%m-%d')
                six_months_ago = datetime.now() - timedelta(days=180)
                if pub_date < six_months_ago:
                    return False
            except:
                pass  # If date parsing fails, include the paper
        
        # Enhanced relevance score filtering (as requested: > 6.5)
        relevance_score = paper.get('relevance_score', 0)
        
        # High threshold for general papers
        if relevance_score > 6.5:
            return True
        
        # Medium threshold for papers from top organizations
        if paper.get('has_top_org', False) and relevance_score > 4.0:
            return True
        
        # Lower threshold only for specific high-value keywords
        high_value_keywords = ['deepmind', 'openai', 'anthropic', 'robotics', 'humanoid', '1x']
        if any(keyword in paper.get('title', '').lower() for keyword in high_value_keywords):
            return relevance_score > 3.0
        
        return False
    
    def _calculate_relevance(self, title: str, abstract: str, tasks: List[str], 
                           methods: List[str], query: str) -> float:
        """Calculate enhanced relevance score with focus on high-impact research"""
        score = 0.0
        
        title_lower = title.lower()
        abstract_lower = abstract.lower()
        query_lower = query.lower()
        full_text = f"{title_lower} {abstract_lower}"
        
        # Query term in title (highest weight)
        if query_lower in title_lower:
            score += 4.0
        
        # Query term in abstract
        if query_lower in abstract_lower:
            score += 2.0
        
        # High-value organization/company keywords (as requested)
        high_value_orgs = {
            'deepmind': 3.0, 'openai': 3.0, 'anthropic': 2.5, 'google': 2.0,
            'microsoft': 2.0, 'nvidia': 2.5, 'tesla': 2.5, 'meta': 2.0,
            'stanford': 2.0, 'mit': 2.0, 'berkeley': 2.0, 'cmu': 2.0,
            'boston dynamics': 3.0, 'sanctuary ai': 3.0, '1x technologies': 3.0,
            'figure ai': 3.0, 'autonomous': 2.0, 'robotics': 2.0
        }
        
        for org, weight in high_value_orgs.items():
            if org in full_text:
                score += weight
        
        # Top organization bonus (additional)
        if self._check_top_organization(title, abstract):
            score += 1.5
        
        # Task relevance with higher weights for robotics/AI
        high_impact_tasks = {
            'robotics': 3.0, 'autonomous-driving': 3.0, 'reinforcement-learning': 2.5,
            'language-modeling': 2.0, 'computer-vision': 1.5, 'object-detection': 1.5,
            'human-pose-estimation': 2.0, 'natural-language-processing': 2.0,
            'machine-translation': 1.5, 'question-answering': 1.5
        }
        
        task_text = ' '.join(tasks).lower()
        for task, weight in high_impact_tasks.items():
            if task in task_text:
                score += weight
        
        # Method relevance with focus on modern approaches
        cutting_edge_methods = {
            'transformer': 2.0, 'foundation model': 2.5, 'diffusion': 2.0,
            'attention mechanism': 1.5, 'multimodal': 2.0, 'few-shot': 1.5,
            'zero-shot': 1.5, 'reinforcement learning': 2.0, 'neural network': 1.0,
            'deep learning': 1.0, 'gpt': 2.0, 'bert': 1.5, 'llama': 2.0
        }
        
        method_text = ' '.join(methods).lower()
        for method, weight in cutting_edge_methods.items():
            if method in method_text:
                score += weight
        
        # Advanced AI/robotics terms with higher emphasis
        advanced_ai_terms = {
            'foundation model': 2.5, 'large language model': 2.0, 'multimodal': 2.0,
            'embodied ai': 3.0, 'humanoid': 3.0, 'autonomous': 2.0,
            'policy gradient': 2.0, 'imitation learning': 2.0, 'sim-to-real': 2.5,
            'robot learning': 3.0, 'manipulation': 2.0, 'navigation': 1.5,
            'reasoning': 2.0, 'planning': 1.5, 'control': 1.5
        }
        
        for term, weight in advanced_ai_terms.items():
            if term in full_text:
                score += weight
        
        # Add type classification tags for clustering
        paper_type = self._classify_paper_type(title, abstract, tasks, methods)
        
        return score
    
    def _check_top_organization(self, title: str, abstract: str) -> bool:
        """Check if paper is from a top AI organization"""
        
        full_text = f"{title.lower()} {abstract.lower()}"
        
        top_orgs = [
            'deepmind', 'openai', 'anthropic', 'google', 'meta', 'microsoft',
            'stanford', 'mit', 'berkeley', 'carnegie mellon', 'cmu',
            'boston dynamics', 'sanctuary ai', '1x technologies', '1x',
            'tesla', 'nvidia', 'fair', 'google research', 'harvard',
            'princeton', 'yale', 'caltech', 'eth zurich', 'toronto',
            'mila', 'oxford', 'cambridge', 'imperial college'
        ]
        
        return any(org in full_text for org in top_orgs)
    
    def _classify_paper_type(self, title: str, abstract: str, tasks: List[str], methods: List[str]) -> str:
        """Classify paper type for clustering (as requested)"""
        full_text = f"{title.lower()} {abstract.lower()}"
        
        # Classification rules based on content
        if any(term in full_text for term in ['translation', 'machine translation', 'multilingual']):
            return 'type:Translation'
        elif any(term in full_text for term in ['foundation model', 'large language model', 'llm']):
            return 'type:Foundation Model'
        elif any(term in full_text for term in ['robot', 'robotics', 'manipulation', 'navigation']):
            return 'type:Robotics'
        elif any(term in full_text for term in ['autonomous', 'self-driving', 'driving']):
            return 'type:Autonomous Systems'
        elif any(term in full_text for term in ['computer vision', 'image', 'visual']):
            return 'type:Computer Vision'
        elif any(term in full_text for term in ['reinforcement learning', 'policy', 'rl']):
            return 'type:Reinforcement Learning'
        elif any(term in full_text for term in ['multimodal', 'vision-language']):
            return 'type:Multimodal'
        else:
            return 'type:General AI'
    
    def monitor_all_keywords(self) -> List[Dict[str, Any]]:
        """Monitor all configured Papers With Code keywords for recent papers"""
        all_papers = []
        keyword_stats = {}
        
        logger.info("Starting Papers With Code paper monitoring...")
        
        for keyword in PAPERSWITHCODE_KEYWORDS:
            logger.info(f"Searching Papers With Code for keyword: {keyword}")
            try:
                papers = self.search_papers(keyword)
                keyword_stats[keyword] = len(papers)
                all_papers.extend(papers)
                
                # Respectful delay between requests
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Failed to search for keyword '{keyword}': {e}")
                keyword_stats[keyword] = 0
                continue
        
        # Log keyword statistics
        logger.info("Papers With Code keyword search results:")
        for keyword, count in keyword_stats.items():
            logger.info(f"  {keyword}: {count} papers")
        
        # Remove duplicates based on title
        unique_papers = self._remove_duplicates(all_papers)
        
        # Sort by relevance score and top organization
        unique_papers.sort(key=lambda x: (x['has_top_org'], x['relevance_score']), reverse=True)
        
        # Log top organizations found
        top_org_papers = [p for p in unique_papers if p['has_top_org']]
        logger.info(f"Found {len(top_org_papers)} papers from top organizations")
        
        logger.info(f"Papers With Code monitoring complete. Found {len(unique_papers)} unique papers")
        return unique_papers[:15]  # Return top 15 papers
    
    def _remove_duplicates(self, papers: List[Dict]) -> List[Dict]:
        """Remove duplicate papers based on title"""
        unique_papers = []
        seen_titles = set()
        
        for paper in papers:
            title_key = paper['title'].lower().strip()
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_papers.append(paper)
        
        return unique_papers

if __name__ == "__main__":
    monitor = PapersWithCodeMonitor()
    papers = monitor.monitor_all_keywords()
    print(f"Found {len(papers)} papers")
    for paper in papers[:3]:
        print(f"- {paper['title']} (Score: {paper['relevance_score']:.1f})")
        print(f"  Tasks: {paper['tasks']}")
        print(f"  Methods: {paper['methods']}")
        print(f"  Top org: {paper['has_top_org']}")
        print() 