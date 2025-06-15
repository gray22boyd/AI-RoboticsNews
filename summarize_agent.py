#!/usr/bin/env python3
"""
Advanced Intelligent Summarize Agent
Creates clustered AI & robotics digest using GPT-4 with full content extraction and context-aware analysis
"""

import logging
from typing import List, Dict, Any, Tuple
import json
from collections import defaultdict
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import concurrent.futures
from openai import OpenAI
from config import OPENAI_API_KEY
from utils import truncate_text, format_date_readable, rate_limit

logger = logging.getLogger(__name__)

class IntelligentSummarizeAgent:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Setup session for web scraping
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        })
        
        # Topic clustering definitions
        self.topic_clusters = {
            'openai': {
                'keywords': ['openai', 'chatgpt', 'gpt-4', 'gpt-5', 'dall-e', 'whisper', 'o1'],
                'display_name': '🧠 OpenAI & ChatGPT',
                'icon': '🧠'
            },
            'deepmind': {
                'keywords': ['deepmind', 'gemini', 'bard', 'alphafold', 'alphacode'],
                'display_name': '🔬 DeepMind & Google AI',
                'icon': '🔬'
            },
            'humanoids': {
                'keywords': ['humanoid', 'figure ai', 'sanctuary ai', '1x technologies', 'boston dynamics', 'atlas'],
                'display_name': '🤖 Humanoids & Physical AI',
                'icon': '🤖'
            },
            'tesla_nvidia': {
                'keywords': ['tesla', 'nvidia', 'fsd', 'autonomous', 'self-driving', 'cuda'],
                'display_name': '🚗 Tesla & NVIDIA AI',
                'icon': '🚗'
            },
            'anthropic': {
                'keywords': ['anthropic', 'claude', 'constitutional ai'],
                'display_name': '🤝 Anthropic & Claude',
                'icon': '🤝'
            },
            'regulation_ethics': {
                'keywords': ['regulation', 'ethics', 'safety', 'bias', 'privacy', 'gdpr', 'ai act'],
                'display_name': '⚖️ AI Regulation & Ethics',
                'icon': '⚖️'
            },
            'research_models': {
                'keywords': ['transformer', 'llm', 'foundation model', 'multimodal', 'reasoning'],
                'display_name': '📚 Foundation Models & Research',
                'icon': '📚'
            },
            'robotics_automation': {
                'keywords': ['robotics', 'automation', 'industrial', 'manufacturing', 'ros'],
                'display_name': '🏭 Robotics & Automation',
                'icon': '🏭'
            },
            'general_ai': {
                'keywords': ['artificial intelligence', 'machine learning', 'neural network', 'deep learning'],
                'display_name': '📊 General AI Research',
                'icon': '📊'
            }
        }
        
        # Content tags for classification
        self.content_tags = {
            'breakthrough': ['breakthrough', 'first time', 'revolutionary', 'milestone', 'record'],
            'privacy': ['privacy', 'data protection', 'gdpr', 'surveillance', 'personal data'],
            'deployment': ['deployment', 'production', 'commercial', 'enterprise', 'scaling'],
            'research': ['research', 'study', 'paper', 'findings', 'experiment'],
            'funding': ['funding', 'investment', 'series', 'valuation', 'acquisition'],
            'open_source': ['open source', 'github', 'repository', 'community', 'free']
        }
    
    @rate_limit(calls_per_minute=30)  # Be respectful to websites
    def extract_full_article_content(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        """Extract full article content from URL using BeautifulSoup"""
        try:
            logger.info(f"Extracting content from: {url}")
            
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'advertisement', 'iframe']):
                element.decompose()
            
            # Try to find main content area with multiple selectors
            content_selectors = [
                'article', '[role="main"]', '.article-content', '.post-content', 
                '.entry-content', '.content', 'main', '.article-body', '.story-body',
                '.post-body', '.article-text', '.content-body'
            ]
            
            content_text = ""
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    content_text = content_elem.get_text(separator=' ', strip=True)
                    if len(content_text) > 500:  # Good content found
                        break
            
            # Fallback to body if no specific content area found
            if not content_text or len(content_text) < 200:
                content_text = soup.body.get_text(separator=' ', strip=True) if soup.body else ""
            
            # Clean up text
            content_text = re.sub(r'\s+', ' ', content_text)
            content_text = re.sub(r'Advertisement|Subscribe|Sign up|Newsletter', '', content_text, flags=re.IGNORECASE)
            
            # Extract title
            title = ""
            if soup.title:
                title = soup.title.string.strip()
            elif soup.find('h1'):
                title = soup.find('h1').get_text(strip=True)
            
            # Extract publish date
            publish_date = ""
            date_selectors = ['time', '[datetime]', '.date', '.published', '.post-date']
            for selector in date_selectors:
                date_elem = soup.select_one(selector)
                if date_elem:
                    publish_date = date_elem.get('datetime') or date_elem.get_text(strip=True)
                    break
            
            return {
                'content': content_text,
                'title': title,
                'publish_date': publish_date,
                'word_count': len(content_text.split()),
                'extraction_success': len(content_text) > 200,
                'url': url
            }
            
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}")
            return {
                'content': '', 
                'extraction_success': False, 
                'error': str(e),
                'url': url
            }

    def enrich_articles_with_content(self, articles: List[Dict[str, Any]], max_articles: int = 5) -> List[Dict[str, Any]]:
        """Extract full content from top articles"""
        enriched_articles = []
        
        # Sort by relevance and take top articles
        sorted_articles = sorted(articles, key=lambda x: x.get('relevance_score', 0), reverse=True)[:max_articles]
        
        for article in sorted_articles:
            url = article.get('url', '')
            if not url:
                continue
                
            logger.info(f"Extracting content from: {article.get('title', 'Unknown')[:50]}...")
            
            # Extract full content
            content_data = self.extract_full_article_content(url)
            
            if content_data.get('extraction_success'):
                # Merge original article with extracted content
                enriched_article = {**article}
                enriched_article.update(content_data)
                enriched_articles.append(enriched_article)
                logger.info(f"✅ Extracted {content_data.get('word_count', 0)} words")
            else:
                logger.warning(f"❌ Failed to extract content from: {article.get('title', 'Unknown')[:50]}")
                # Still include article with original data
                enriched_articles.append(article)
        
        return enriched_articles

    def _make_gpt_request(self, prompt: str, max_tokens: int = 300, temperature: float = 0.3) -> str:
        """Make GPT request with proper error handling and truncation detection"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            content = response.choices[0].message.content.strip()
            finish_reason = response.choices[0].finish_reason
            
            # Check if response was truncated
            if finish_reason == "length":
                logger.warning("GPT response was truncated, retrying with higher token limit")
                # Retry with more tokens
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens * 2,
                    temperature=temperature
                )
                content = response.choices[0].message.content.strip()
                
            return content
            
        except Exception as e:
            logger.error(f"GPT request failed: {e}")
            return "Analysis temporarily unavailable due to processing error."
    
    def cluster_items_by_topic(self, items: List[Dict[str, Any]], text_fields: List[str]) -> Dict[str, List[Dict]]:
        """Cluster items by topic based on content analysis"""
        clusters = defaultdict(list)
        unclustered = []
        
        for item in items:
            # Combine text fields for analysis
            full_text = " ".join([
                str(item.get(field, '')) for field in text_fields
            ]).lower()
            
            # Find best matching cluster
            best_cluster = None
            max_matches = 0
            
            for cluster_id, cluster_info in self.topic_clusters.items():
                matches = sum(1 for keyword in cluster_info['keywords'] if keyword in full_text)
                if matches > max_matches:
                    max_matches = matches
                    best_cluster = cluster_id
            
            if best_cluster and max_matches > 0:
                clusters[best_cluster].append(item)
            else:
                unclustered.append(item)
        
        # Add unclustered high-relevance items to general category
        if unclustered:
            high_relevance = [item for item in unclustered if item.get('relevance_score', 0) > 3.0]
            if high_relevance:
                clusters['general_ai'] = high_relevance
        
        return dict(clusters)
    
    def extract_content_tags(self, text: str) -> List[str]:
        """Extract content classification tags from text"""
        text_lower = text.lower()
        found_tags = []
        
        for tag, keywords in self.content_tags.items():
            if any(keyword in text_lower for keyword in keywords):
                found_tags.append(tag)
        
        return found_tags
    
    def analyze_github_clusters(self, github_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze GitHub commits with clustering and intelligence"""
        try:
            commits = github_data.get('commits', [])
            if not commits:
                return {'status': 'no_data', 'message': 'No GitHub commits found in monitoring period.'}
            
            # Cluster commits by topic
            clustered_commits = self.cluster_items_by_topic(
                commits, 
                ['message', 'repo', 'author']
            )
            
            if not clustered_commits:
                return {'status': 'no_relevant', 'message': 'No relevant GitHub activity detected.'}
            
            analysis_results = {}
            
            for cluster_id, cluster_commits in clustered_commits.items():
                if len(cluster_commits) < 1:  # Allow single commits for analysis
                    continue
                
                cluster_info = self.topic_clusters.get(cluster_id, {
                    'display_name': '💻 Other Development',
                    'icon': '💻'
                })
                
                # Prepare detailed commit data for analysis
                commit_details = []
                for commit in cluster_commits[:8]:  # Analyze up to 8 commits
                    commit_details.append({
                        'repo': commit.get('repo', 'unknown'),
                        'message': commit.get('message', '')[:150],
                        'author': commit.get('author', ''),
                        'files_changed': commit.get('files_changed', 0)
                    })
                
                prompt = f"""
                Analyze these GitHub commits for {cluster_info['display_name']} on {datetime.now().strftime("%B %d, %Y")}:
                
                Commits: {json.dumps(commit_details, indent=2)}
                
                CRITICAL CONTEXT:
                - Today's date is {datetime.now().strftime("%B %d, %Y")}
                - You are analyzing recent development activity in AI and robotics
                - Focus on what developers are actually working on NOW
                
                Provide a technical analysis focusing on:
                1. What specific functionality is being developed/improved
                2. Key technical changes or architectural decisions
                3. Impact on users or developers
                
                Format: Write 2-3 sentences describing the main development themes, then list exactly 2-3 specific changes as bullets:
                - Each bullet must describe a concrete technical change
                - Be specific about what was modified/added/fixed
                - If commits are unclear/minor, focus on the repository areas being worked on
                - Maximum 1 line per bullet point
                
                Example good format:
                "PyTorch development focused on improving dynamic execution and XPU support this week. The team made significant updates to the Dynamo tracing system and expanded hardware compatibility.
                - Added XPU API support to trace_rules for better hardware acceleration
                - Implemented helper functions for guard filter hooks in dynamic execution
                - Updated gradient behavior documentation for torch.amin and torch.amax functions"
                
                Do not use markdown headers or labels like "**Analysis:**"
                """
                
                analysis = self._make_gpt_request(prompt, max_tokens=250, temperature=0.2)
                
                analysis_results[cluster_id] = {
                    'cluster_info': cluster_info,
                    'commit_count': len(cluster_commits),
                    'analysis': analysis,
                    'raw_commits': cluster_commits[:3]  # Keep top 3 for sources
                }
            
            return {'status': 'success', 'clusters': analysis_results}
            
        except Exception as e:
            logger.error(f"Error analyzing GitHub clusters: {e}")
            return {'status': 'error', 'message': 'GitHub analysis unavailable due to processing error.'}
    
    def analyze_paper_clusters(self, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze research papers with clustering and relevance filtering"""
        try:
            if not papers:
                return {'status': 'no_data', 'message': 'No research papers found in monitoring period.'}
            
            # Filter for high-relevance papers
            relevant_papers = [p for p in papers if p.get('relevance_score', 0) >= 6.0]
            
            if not relevant_papers:
                return {'status': 'no_relevant', 'message': 'No high-relevance papers found.'}
            
            # Cluster papers by topic
            clustered_papers = self.cluster_items_by_topic(
                relevant_papers,
                ['title', 'abstract', 'keywords']
            )
            
            if not clustered_papers:
                return {'status': 'no_clusters', 'message': 'Papers could not be meaningfully clustered.'}
            
            analysis_results = {}
            
            for cluster_id, cluster_papers in clustered_papers.items():
                if len(cluster_papers) < 1:
                    continue
                
                cluster_info = self.topic_clusters.get(cluster_id, {
                    'display_name': '📄 Research Papers',
                    'icon': '📄'
                })
                
                # Prepare paper data for analysis
                paper_data = []
                for paper in cluster_papers[:6]:  # Max 6 papers per cluster
                    paper_data.append({
                        'title': paper.get('title', '')[:100],
                        'abstract': paper.get('abstract', '')[:300] if paper.get('abstract') else '',
                        'relevance': paper.get('relevance_score', 0)
                    })
                
                prompt = f"""
                Analyze these research papers for {cluster_info['display_name']} on {datetime.now().strftime("%B %d, %Y")}:
                
                Papers: {json.dumps(paper_data, indent=2)}
                
                CRITICAL CONTEXT:
                - Today's date is {datetime.now().strftime("%B %d, %Y")}
                - You are analyzing recent research developments in AI and robotics
                - Focus on what researchers are working on NOW in {datetime.now().year}
                
                Provide an insightful analysis focusing on:
                1. What research problems are being addressed
                2. Key methodological approaches or innovations
                3. Potential real-world applications or implications
                
                Format: Write 2-3 sentences describing the research direction and significance, then list exactly 2-3 key papers as bullets:
                - Each bullet: "Paper Title" — Brief description of contribution/innovation (1 line max)
                - Focus on what makes each paper significant or novel
                - Explain potential impact or applications
                
                Example good format:
                "The research focuses on improving autonomous navigation through advanced sensor fusion and AI reasoning. These papers address critical challenges in real-world deployment of autonomous systems.
                - "OctoNav: Towards Generalist Embodied Navigation" — Develops unified navigation framework bridging different robotic tasks and environmental conditions
                - "Event-based Camera Navigation with RL" — Combines event cameras with reinforcement learning for real-time obstacle avoidance in dynamic environments"
                
                Do not use markdown headers. Be specific about technical contributions.
                """
                
                analysis = self._make_gpt_request(prompt, max_tokens=300, temperature=0.3)
                
                analysis_results[cluster_id] = {
                    'cluster_info': cluster_info,
                    'paper_count': len(cluster_papers),
                    'analysis': analysis,
                    'raw_papers': cluster_papers[:3]
                }
            
            return {'status': 'success', 'clusters': analysis_results}
            
        except Exception as e:
            logger.error(f"Error analyzing paper clusters: {e}")
            return {'status': 'error', 'message': 'Paper analysis unavailable due to processing error.'}
    
    def analyze_news_clusters(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze news articles with full content extraction and context-aware analysis"""
        try:
            if not articles:
                return {'status': 'no_data', 'message': 'No news articles found in monitoring period.'}
            
            # Cluster articles by topic
            clustered_articles = self.cluster_items_by_topic(
                articles,
                ['title', 'description', 'content']
            )
            
            if not clustered_articles:
                return {'status': 'no_clusters', 'message': 'No clusterable news found.'}
            
            analysis_results = {}
            current_date = datetime.now().strftime("%B %d, %Y")
            
            for cluster_id, cluster_articles in clustered_articles.items():
                if len(cluster_articles) < 1:
                    continue
                    
                cluster_info = self.topic_clusters.get(cluster_id, {
                    'display_name': '📰 Tech News',
                    'icon': '📰'
                })
                
                logger.info(f"Analyzing {len(cluster_articles)} articles for {cluster_info['display_name']}")
                
                # Extract full content from top articles
                enriched_articles = self.enrich_articles_with_content(cluster_articles, max_articles=3)
                
                if not enriched_articles:
                    logger.warning(f"No articles available for cluster: {cluster_info['display_name']}")
                    continue
                
                # Create detailed analysis prompt with full content
                article_content = []
                for i, article in enumerate(enriched_articles, 1):
                    content = article.get('content', '')
                    if len(content) > 2000:
                        content = content[:2000] + '...'
                    elif len(content) < 100:
                        # Use description if content extraction failed
                        content = article.get('description', 'Content not available')
                    
                    article_content.append(f"""
Article {i}: {article.get('title', 'Unknown')}
Source: {article.get('source', 'Unknown')} | Published: {article.get('published_at', 'Recent')}
Content: {content}
URL: {article.get('url', '')}
""")
                
                prompt = f"""
You are analyzing AI and robotics news on {current_date}. 

Topic: {cluster_info['display_name']}

Here are the full articles with actual content:

{''.join(article_content)}

CRITICAL CONTEXT:
- Today's date is {current_date} (NOT 2023!)
- You are analyzing recent developments in AI and robotics
- Base your analysis ONLY on the actual article content provided above
- Be specific about companies, products, technical details, and dates mentioned in the articles

Provide analysis focusing on:
1. What specific business developments or technical advances are happening
2. Key product launches, partnerships, or strategic announcements
3. Concrete details from the articles (names, numbers, dates, capabilities)

Format: Write 2-3 sentences describing what's actually happening based on the article content, then list exactly 2-3 key developments as bullets:
- Each bullet: *Company/Product* — Specific development from the articles with concrete details (1 line max)
- Include specific metrics, dates, or technical capabilities mentioned in the articles
- Focus on what's NEW or ANNOUNCED, not general background

Example format:
"Microsoft has integrated advanced AI capabilities into its developer tools, while NVIDIA announced new partnerships for autonomous vehicle development. These moves represent concrete steps toward enterprise AI adoption in {current_date.split(',')[1].strip()}.
- *Microsoft Copilot* — Launched new code generation features with 40% faster debugging capabilities for Visual Studio users
- *NVIDIA Drive* — Announced partnership with Mercedes-Benz to deploy AI-powered autonomous driving systems in 2025 models
- *OpenAI Enterprise* — Released API updates enabling real-time voice interactions for business applications"

Base everything on the actual article content provided. Do not make up details not in the articles.
"""
                
                analysis = self._make_gpt_request(prompt, max_tokens=400, temperature=0.2)
                
                analysis_results[cluster_id] = {
                    'cluster_info': cluster_info,
                    'article_count': len(cluster_articles),
                    'analysis': analysis,
                    'raw_articles': enriched_articles[:2],  # Keep top 2 with full content
                    'content_extracted': True
                }
            
            return {'status': 'success', 'clusters': analysis_results}
            
        except Exception as e:
            logger.error(f"Error analyzing news clusters: {e}")
            return {'status': 'error', 'message': 'News analysis unavailable due to processing error.'}
    
    def generate_cross_cluster_insights(self, github_analysis: Dict, papers_analysis: Dict, news_analysis: Dict) -> str:
        """Generate strategic insights across all data clusters using GPT analysis"""
        try:
            # Extract successful clusters with actual content
            github_clusters = github_analysis.get('clusters', {}) if github_analysis.get('status') == 'success' else {}
            papers_clusters = papers_analysis.get('clusters', {}) if papers_analysis.get('status') == 'success' else {}
            news_clusters = news_analysis.get('clusters', {}) if news_analysis.get('status') == 'success' else {}
            
            if not (github_clusters or papers_clusters or news_clusters):
                return "Limited cross-topic patterns identified today due to insufficient data across sources."
            
            # Prepare comprehensive data for GPT analysis
            strategic_data = {
                'github_insights': {},
                'research_insights': {},
                'industry_insights': {},
                'cross_topic_patterns': {}
            }
            
            # Extract GitHub development patterns
            for cluster_id, cluster_data in github_clusters.items():
                strategic_data['github_insights'][cluster_id] = {
                    'topic': cluster_data['cluster_info']['display_name'],
                    'commit_count': cluster_data['commit_count'],
                    'analysis': cluster_data['analysis'],
                    'sample_commits': [commit.get('message', '')[:100] for commit in cluster_data.get('raw_commits', [])[:3]]
                }
            
            # Extract research trends
            for cluster_id, cluster_data in papers_clusters.items():
                strategic_data['research_insights'][cluster_id] = {
                    'topic': cluster_data['cluster_info']['display_name'],
                    'paper_count': cluster_data['paper_count'],
                    'analysis': cluster_data['analysis'],
                    'sample_papers': [paper.get('title', '')[:100] for paper in cluster_data.get('raw_papers', [])[:2]]
                }
            
            # Extract industry developments
            for cluster_id, cluster_data in news_clusters.items():
                strategic_data['industry_insights'][cluster_id] = {
                    'topic': cluster_data['cluster_info']['display_name'],
                    'article_count': cluster_data['article_count'],
                    'analysis': cluster_data['analysis'],
                    'sample_headlines': [article.get('title', '')[:100] for article in cluster_data.get('raw_articles', [])[:3]]
                }
            
            # Identify cross-topic patterns
            all_topics = set(github_clusters.keys()) | set(papers_clusters.keys()) | set(news_clusters.keys())
            for topic in all_topics:
                if sum(1 for source in [github_clusters, papers_clusters, news_clusters] if topic in source) >= 2:
                    strategic_data['cross_topic_patterns'][topic] = {
                        'has_development': topic in github_clusters,
                        'has_research': topic in papers_clusters,
                        'has_industry_news': topic in news_clusters,
                        'convergence_strength': sum(1 for source in [github_clusters, papers_clusters, news_clusters] if topic in source)
                    }
            
            # Generate GPT-powered strategic analysis
            prompt = f"""
            You are analyzing AI intelligence data on {datetime.now().strftime("%B %d, %Y")} (NOT 2023!).

            Analyze this data to identify strategic patterns:

            {json.dumps(strategic_data, indent=2)}

            CRITICAL CONTEXT:
            - Today's date is {datetime.now().strftime("%B %d, %Y")}
            - You are analyzing current developments in AI and robotics
            - Focus on what's happening NOW in {datetime.now().year}
            - Provide actionable intelligence for current business decisions

            Write exactly 3-4 sentences revealing strategic insights by connecting developments across sectors.

            Focus on:
            - Cross-sector implications connecting different companies/technologies
            - Current timing signals for technology adoption in {datetime.now().year}
            - Competitive positioning shifts happening now
            - Immediate business implications for {datetime.now().year}

            Requirements:
            - Maximum 4 sentences total
            - Each insight must connect at least 2 different sectors/companies
            - Include specific implications for business stakeholders
            - End with actionable intelligence for {datetime.now().year}
            - Do NOT reference 2023 or any past years

            Example format:
            "The convergence of NVIDIA's enterprise AI expansion and OpenAI's multimodal capabilities signals accelerated enterprise AI adoption in Q1 {datetime.now().year}. Technical teams should evaluate integrated AI infrastructure solutions while legal teams prepare for updated AI governance frameworks. The simultaneous focus on autonomous systems safety indicates physical AI deployment timelines are advancing faster than expected, requiring immediate workforce transition planning for {datetime.now().year}."

            Write 3-4 complete sentences about current {datetime.now().year} developments. No bullet points.
            """
            
            strategic_insights = self._make_gpt_request(prompt, max_tokens=250, temperature=0.3)
            
            # Ensure complete sentences
            if strategic_insights and not strategic_insights.endswith('.'):
                # Find the last complete sentence
                last_period = strategic_insights.rfind('.')
                if last_period > 0:
                    strategic_insights = strategic_insights[:last_period + 1]
            
            return strategic_insights
            
        except Exception as e:
            logger.error(f"Error generating cross-cluster insights: {e}")
            return "Strategic analysis unavailable due to processing limitations."
    
    def create_intelligent_digest(self, 
                                github_data: Dict[str, Any], 
                                papers_data: List[Dict[str, Any]], 
                                news_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create complete intelligent digest with clustering and analysis"""
        try:
            logger.info("🧠 Starting intelligent clustering and analysis...")
            
            # Analyze each data source with clustering
            github_analysis = self.analyze_github_clusters(github_data)
            papers_analysis = self.analyze_paper_clusters(papers_data)
            news_analysis = self.analyze_news_clusters(news_data)
            
            # Generate cross-cluster strategic insights
            strategic_insights = self.generate_cross_cluster_insights(
                github_analysis, papers_analysis, news_analysis
            )
            
            logger.info("✅ Intelligent analysis complete")
            
            return {
                'github_analysis': github_analysis,
                'papers_analysis': papers_analysis, 
                'news_analysis': news_analysis,
                'strategic_insights': strategic_insights,
                'timestamp': datetime.now().strftime("%B %d, %Y at %I:%M %p")
            }
            
        except Exception as e:
            logger.error(f"Error creating intelligent digest: {e}")
            return {
                'error': 'Intelligent digest creation failed',
                'message': str(e),
                'timestamp': datetime.now().strftime("%B %d, %Y at %I:%M %p")
            }

# Backwards compatibility
class SummarizeAgent(IntelligentSummarizeAgent):
    """Backwards compatible wrapper"""
    
    def create_concise_digest(self, github_data: Dict, papers_data: List, news_data: List) -> str:
        """Legacy method that returns HTML for email"""
        from email_agent import IntelligentEmailAgent
        
        # Get intelligent analysis
        digest_data = self.create_intelligent_digest(github_data, papers_data, news_data)
        
        # Use email agent to format
        email_agent = IntelligentEmailAgent()
        return email_agent.create_intelligent_email_content(digest_data, github_data, papers_data, news_data)

if __name__ == "__main__":
    # Test the intelligent clustering
    agent = IntelligentSummarizeAgent()
    
    # Mock test data
    test_commits = [
        {'repo': 'pytorch/pytorch', 'message': 'Add CUDA kernel optimization', 'author': 'dev1'},
        {'repo': 'huggingface/transformers', 'message': 'Update GPT model config', 'author': 'dev2'}
    ]
    test_papers = [
        {'title': 'Attention Is All You Need Revisited', 'relevance_score': 7.0, 'abstract': 'New transformer analysis'}
    ]
    test_news = [
        {'title': 'OpenAI Releases GPT-5', 'description': 'Major breakthrough', 'relevance_score': 8.0}
    ]
    
    result = agent.create_intelligent_digest(
        {'commits': test_commits},
        test_papers,
        test_news
    )
    
    print("🧠 Intelligent Analysis Result:")
    print(json.dumps(result, indent=2)) 