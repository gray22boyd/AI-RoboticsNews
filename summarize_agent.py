#!/usr/bin/env python3
"""
Intelligent Summarize Agent
Creates clustered AI & robotics digest using GPT-4 with topic grouping and relevance filtering
"""

import logging
from typing import List, Dict, Any, Tuple
import json
from collections import defaultdict
import re
from datetime import datetime
from openai import OpenAI
from config import OPENAI_API_KEY
from utils import truncate_text, format_date_readable

logger = logging.getLogger(__name__)

class IntelligentSummarizeAgent:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
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
                clusters['other'] = high_relevance
        
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
                if len(cluster_commits) < 2:  # Skip clusters with too few items
                    continue
                
                cluster_info = self.topic_clusters.get(cluster_id, {
                    'display_name': '💻 Other Development',
                    'icon': '💻'
                })
                
                # Prepare data for GPT analysis
                commit_data = []
                repo_summary = defaultdict(list)
                
                for commit in cluster_commits[:5]:  # Max 5 commits per cluster
                    repo = commit.get('repo', 'unknown')
                    repo_summary[repo].append({
                        'message': commit.get('message', '')[:100],
                        'author': commit.get('author', '')
                    })
                
                prompt = f"""
                Analyze these GitHub commits for {cluster_info['display_name']}:
                
                Repository Activity: {json.dumps(dict(repo_summary), indent=2)}
                
                Create a natural summary without markdown labels:
                
                Write 1-2 sentences describing the main development themes, then list 2-3 specific technical changes as short bullets:
                - Focus on actual changes visible in commit messages
                - Be technically specific, not generic
                - If commits are minor/unclear, state "Minor maintenance updates across repositories"
                - Each bullet point must be 1 line maximum
                - Group similar changes together
                
                Do not use **Headline:** or **Key Changes:** labels.
                """
                
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200,
                    temperature=0.2
                )
                
                analysis_results[cluster_id] = {
                    'cluster_info': cluster_info,
                    'commit_count': len(cluster_commits),
                    'analysis': response.choices[0].message.content.strip(),
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
            
            # Filter by relevance score > 6.5 as requested
            high_relevance_papers = [p for p in papers if p.get('relevance_score', 0) > 6.5]
            
            if not high_relevance_papers:
                # Check if we have any papers with score > 4.0
                medium_papers = [p for p in papers if p.get('relevance_score', 0) > 4.0]
                if not medium_papers:
                    return {'status': 'no_relevant', 'message': 'No papers meeting relevance threshold found today.'}
                high_relevance_papers = medium_papers[:3]
            
            # Cluster papers by topic
            clustered_papers = self.cluster_items_by_topic(
                high_relevance_papers,
                ['title', 'abstract', 'query']
            )
            
            if not clustered_papers:
                return {'status': 'no_clusters', 'message': 'No clusterable papers found.'}
            
            analysis_results = {}
            
            for cluster_id, cluster_papers in clustered_papers.items():
                cluster_info = self.topic_clusters.get(cluster_id, {
                    'display_name': '📊 General AI Research',
                    'icon': '📊'
                })
                
                # Take top papers from cluster
                top_papers = sorted(cluster_papers, key=lambda x: x.get('relevance_score', 0), reverse=True)[:2]
                
                papers_data = []
                for paper in top_papers:
                    paper_info = {
                        'title': paper.get('title', 'Unknown Title'),
                        'abstract': paper.get('abstract', 'No abstract')[:300],
                        'relevance_score': paper.get('relevance_score', 0),
                        'tasks': paper.get('tasks', []),
                        'methods': paper.get('methods', []),
                        'has_top_org': paper.get('has_top_org', False)
                    }
                    papers_data.append(paper_info)
                
                prompt = f"""
                Analyze these research papers for {cluster_info['display_name']}:
                
                Papers: {json.dumps(papers_data, indent=2)}
                
                Create a natural research summary without markdown labels:
                
                Write 1-2 sentences about the common research direction, then list 2 key findings as short bullets:
                - Focus on concrete technical contributions and real-world applications
                - Highlight practical applications and impact
                - If papers are preliminary/incremental, state honestly
                - Each finding must be 1-2 sentences maximum
                - Use format: *Paper Title* — brief contribution summary
                
                Do not use **Research Theme:** or **Key Findings:** labels.
                """
                
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=250,
                    temperature=0.3
                )
                
                analysis_results[cluster_id] = {
                    'cluster_info': cluster_info,
                    'paper_count': len(cluster_papers),
                    'analysis': response.choices[0].message.content.strip(),
                    'raw_papers': top_papers
                }
            
            return {'status': 'success', 'clusters': analysis_results}
            
        except Exception as e:
            logger.error(f"Error analyzing paper clusters: {e}")
            return {'status': 'error', 'message': 'Research paper analysis unavailable due to processing error.'}
    
    def analyze_news_clusters(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze news with clustering and topic grouping"""
        try:
            if not articles:
                return {'status': 'no_data', 'message': 'No AI/robotics news found in monitoring period.'}
            
            # Cluster news by topic
            clustered_news = self.cluster_items_by_topic(
                articles,
                ['title', 'description', 'keyword', 'source']
            )
            
            if not clustered_news:
                return {'status': 'no_clusters', 'message': 'No significant news clusters identified.'}
            
            analysis_results = {}
            
            for cluster_id, cluster_articles in clustered_news.items():
                cluster_info = self.topic_clusters.get(cluster_id, {
                    'display_name': '📡 Industry Updates',
                    'icon': '📡'
                })
                
                # Take top articles from cluster
                top_articles = sorted(cluster_articles, key=lambda x: x.get('relevance_score', 0), reverse=True)[:3]
                
                articles_data = []
                for article in top_articles:
                    # Extract content tags
                    full_text = f"{article.get('title', '')} {article.get('description', '')}"
                    tags = self.extract_content_tags(full_text)
                    
                    article_info = {
                        'title': article.get('title', ''),
                        'source': article.get('source', ''),
                        'description': article.get('description', '')[:200],
                        'relevance_score': article.get('relevance_score', 0),
                        'tags': tags
                    }
                    articles_data.append(article_info)
                
                prompt = f"""
                Analyze these news articles for {cluster_info['display_name']}:
                
                Articles: {json.dumps(articles_data, indent=2)}
                
                Create a natural news summary without markdown labels:
                
                Write 1-2 sentences capturing the main industry developments, then list 2-3 key announcements as short bullets:
                - Focus on concrete announcements and business implications
                - Highlight technical and market significance
                - Each development must be 1 line maximum
                - Use format: *Company/Topic* — specific announcement or development
                - Group by company when multiple stories about same organization
                
                Do not use **News Theme:** or **Key Developments:** labels.
                """
                
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300,
                    temperature=0.3
                )
                
                analysis_results[cluster_id] = {
                    'cluster_info': cluster_info,
                    'article_count': len(cluster_articles),
                    'analysis': response.choices[0].message.content.strip(),
                    'raw_articles': top_articles
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
            Analyze this comprehensive AI and robotics intelligence data to identify strategic trends and implications:
            
            Data Summary: {json.dumps(strategic_data, indent=2)}
            
            Synthesize 2-3 sentences about the most significant strategic patterns you observe. Focus on:
            - Cross-sector trends (development + research + industry alignment)
            - Emerging technological shifts or priorities
            - Implications for AI/robotics professionals and organizations
            - Market or competitive dynamics
            
            Write in a professional, analytical tone. Avoid generic statements. Base insights only on the actual data provided. If no meaningful patterns emerge, state that honestly.
            
            Example style: "The convergence of development activity and research focus in humanoid robotics suggests accelerating commercialization timelines. Simultaneously, increased attention to AI safety across both policy discussions and technical implementations indicates growing industry maturity. These trends point to a critical inflection point where theoretical AI capabilities are rapidly transitioning to real-world deployment."
            
            Do not use markdown formatting, bullet points, or section headers.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.4
            )
            
            return response.choices[0].message.content.strip()
            
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