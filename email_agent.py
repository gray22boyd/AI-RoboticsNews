#!/usr/bin/env python3
"""
Intelligent Email Agent for AI News Monitor
Creates dynamic, topic-clustered email content based on intelligent analysis
"""

import logging
from datetime import datetime
from typing import Dict, List, Any
import re
import json

logger = logging.getLogger(__name__)

class IntelligentEmailAgent:
    def __init__(self):
        pass
    
    def create_intelligent_email_content(self, 
                                       digest_data: Dict[str, Any],
                                       github_data: Dict,
                                       papers_data: List,
                                       news_data: List) -> str:
        """Create dynamic email content based on intelligent clustering analysis"""
        try:
            current_date = datetime.now().strftime("%B %d, %Y")
            
            # Check if we have any successful analysis
            github_analysis = digest_data.get('github_analysis', {})
            papers_analysis = digest_data.get('papers_analysis', {})
            news_analysis = digest_data.get('news_analysis', {})
            strategic_insights = digest_data.get('strategic_insights', '')
            
            # Collect all successful topic clusters
            all_clusters = {}
            
            # Add GitHub clusters
            if github_analysis.get('status') == 'success':
                for cluster_id, cluster_data in github_analysis.get('clusters', {}).items():
                    if cluster_id not in all_clusters:
                        all_clusters[cluster_id] = {
                            'info': cluster_data['cluster_info'],
                            'github': cluster_data,
                            'papers': None,
                            'news': None
                        }
            
            # Add Papers clusters
            if papers_analysis.get('status') == 'success':
                for cluster_id, cluster_data in papers_analysis.get('clusters', {}).items():
                    if cluster_id not in all_clusters:
                        all_clusters[cluster_id] = {
                            'info': cluster_data['cluster_info'],
                            'github': None,
                            'papers': cluster_data,
                            'news': None
                        }
                    else:
                        all_clusters[cluster_id]['papers'] = cluster_data
            
            # Add News clusters
            if news_analysis.get('status') == 'success':
                for cluster_id, cluster_data in news_analysis.get('clusters', {}).items():
                    if cluster_id not in all_clusters:
                        all_clusters[cluster_id] = {
                            'info': cluster_data['cluster_info'],
                            'github': None,
                            'papers': None,
                            'news': cluster_data
                        }
                    else:
                        all_clusters[cluster_id]['news'] = cluster_data
            
            html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI & Robotics Intelligence Digest</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f8fafc;
            color: #1a202c;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 700;
        }}
        .header .date {{
            margin-top: 8px;
            opacity: 0.9;
            font-size: 16px;
        }}
        .content {{
            padding: 30px;
        }}
        .topic-section {{
            margin-bottom: 40px;
            border-left: 4px solid #e2e8f0;
            padding-left: 20px;
        }}
        .topic-section.has-data {{
            border-left-color: #4299e1;
        }}
        .topic-title {{
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 15px;
            color: #2d3748;
        }}
        .subsection {{
            margin-bottom: 20px;
            padding: 15px;
            background-color: #f7fafc;
            border-radius: 8px;
            border-left: 3px solid #cbd5e0;
        }}
        .subsection.github {{
            border-left-color: #48bb78;
            background-color: #f0fff4;
        }}
        .subsection.papers {{
            border-left-color: #ed8936;
            background-color: #fffaf0;
        }}
        .subsection.news {{
            border-left-color: #4299e1;
            background-color: #ebf8ff;
        }}
        .subsection-title {{
            font-weight: 600;
            color: #4a5568;
            margin-bottom: 10px;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .analysis-content {{
            font-size: 15px;
            line-height: 1.5;
        }}
        .analysis-content strong {{
            color: #2d3748;
        }}
        .strategic-section {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            margin: 30px 0;
        }}
        .strategic-section h3 {{
            margin-top: 0;
            margin-bottom: 15px;
            font-size: 20px;
        }}
        .executive-summary {{
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 30px;
            border-left: 4px solid #4299e1;
        }}
        .executive-summary h2 {{
            margin-top: 0;
            margin-bottom: 15px;
            font-size: 20px;
            color: #2d3748;
        }}
        .summary-content p {{
            margin-bottom: 15px;
            font-size: 16px;
            color: #4a5568;
        }}
        .summary-bullets {{
            font-size: 15px;
            line-height: 1.6;
        }}
        .summary-bullet {{
            margin-bottom: 8px;
            color: #2d3748;
        }}
        .no-data {{
            text-align: center;
            padding: 40px 20px;
            color: #718096;
            font-style: italic;
        }}
        .sources-section {{
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #e2e8f0;
        }}
        .source-group {{
            margin-bottom: 25px;
        }}
        .source-group h4 {{
            font-size: 16px;
            font-weight: 600;
            color: #4a5568;
            margin-bottom: 10px;
        }}
        .source-item {{
            margin-bottom: 8px;
            padding: 8px 0;
            border-bottom: 1px solid #f1f5f9;
        }}
        .source-item:last-child {{
            border-bottom: none;
        }}
        .source-item a {{
            color: #4299e1;
            text-decoration: none;
            font-weight: 500;
        }}
        .source-item a:hover {{
            text-decoration: underline;
        }}
        .source-meta {{
            font-size: 12px;
            color: #718096;
            margin-top: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI & Robotics Intelligence Digest</h1>
            <div class="date">{current_date}</div>
        </div>
        
        <div class="content">
            {self._generate_executive_summary(all_clusters)}
            
            {self._build_dynamic_content(all_clusters, github_analysis, papers_analysis, news_analysis)}
            
            {self._build_strategic_section(strategic_insights)}
            
            {self._build_sources_section(github_data, papers_data, news_data)}
        </div>
    </div>
</body>
</html>
            """
            
            return html_template
            
        except Exception as e:
            logger.error(f"Error creating intelligent email content: {e}")
            return self._create_fallback_content()
    
    def _build_dynamic_content(self, all_clusters: Dict, github_analysis: Dict, papers_analysis: Dict, news_analysis: Dict) -> str:
        """Build dynamic content sections based on actual topic clusters found"""
        if not all_clusters:
            return self._build_no_data_message()
        
        content_html = ""
        
        # Sort clusters by priority (those with multiple data sources first)
        sorted_clusters = sorted(
            all_clusters.items(),
            key=lambda x: sum(1 for v in [x[1]['github'], x[1]['papers'], x[1]['news']] if v is not None),
            reverse=True
        )
        
        for cluster_id, cluster_data in sorted_clusters:
            cluster_info = cluster_data['info']
            
            content_html += f"""
            <div class="topic-section has-data">
                <div class="topic-title">{self._get_better_topic_heading(cluster_id, cluster_info)}</div>
            """
            
            # Add GitHub subsection if available
            if cluster_data['github']:
                github_analysis_text = cluster_data['github']['analysis']
                content_html += f"""
                <div class="subsection github">
                    <div class="subsection-title">🔧 Development Activity ({cluster_data['github']['commit_count']} commits)</div>
                    <div class="analysis-content">{github_analysis_text}</div>
                </div>
                """
            
            # Add Papers subsection if available
            if cluster_data['papers']:
                papers_analysis_text = cluster_data['papers']['analysis']
                content_html += f"""
                <div class="subsection papers">
                    <div class="subsection-title">📚 Research Papers ({cluster_data['papers']['paper_count']} papers)</div>
                    <div class="analysis-content">{papers_analysis_text}</div>
                </div>
                """
            
            # Add News subsection if available
            if cluster_data['news']:
                news_analysis_text = cluster_data['news']['analysis']
                content_html += f"""
                <div class="subsection news">
                    <div class="subsection-title">📡 Industry News ({cluster_data['news']['article_count']} articles)</div>
                    <div class="analysis-content">{news_analysis_text}</div>
                </div>
                """
            
            content_html += "</div>"
        
        return content_html
    
    def _build_no_data_message(self) -> str:
        """Build message when no clustered data is available"""
        return """
        <div class="no-data">
            <h3>📊 Limited Intelligence Available Today</h3>
            <p>No significant topic clusters were identified across GitHub, research papers, and news sources during this monitoring period. This may indicate a quieter day in AI/robotics developments or requires monitoring additional sources.</p>
        </div>
        """
    
    def _build_strategic_section(self, strategic_insights: str) -> str:
        """Build strategic insights section"""
        if not strategic_insights or strategic_insights.strip() == "":
            return ""
        
        return f"""
        <div class="strategic-section">
            <h3>🎯 Strategic Intelligence</h3>
            <div>{strategic_insights}</div>
        </div>
        """
    
    def _build_sources_section(self, github_data: Dict, papers_data: List, news_data: List) -> str:
        """Build sources section with links to original content"""
        sources_html = '<div class="sources-section"><h3>📋 Sources & References</h3>'
        
        # GitHub Sources
        commits = github_data.get('commits', [])
        if commits:
            sources_html += '<div class="source-group">'
            sources_html += '<h4>🔧 GitHub Commits</h4>'
            
            for commit in commits[:8]:  # Show top 8
                commit_title = self._truncate_text(commit.get('message', 'Unknown commit'), 80)
                commit_url = commit.get('url', '#')
                sources_html += f'''
                <div class="source-item">
                    <a href="{commit_url}" target="_blank">{commit.get('repo', 'unknown')}: {commit_title}</a>
                    <div class="source-meta">by {commit.get('author', 'unknown')} • {commit.get('sha', '')[:8]}</div>
                </div>
                '''
            sources_html += '</div>'
        
        # Research Papers
        if papers_data:
            sources_html += '<div class="source-group">'
            sources_html += '<h4>📚 Research Papers</h4>'
            
            for paper in papers_data[:5]:  # Show top 5
                paper_title = self._truncate_text(paper.get('title', 'Unknown paper'), 100)
                paper_url = paper.get('url', '#')
                relevance = paper.get('relevance_score', 0)
                sources_html += f'''
                <div class="source-item">
                    <a href="{paper_url}" target="_blank">{paper_title}</a>
                    <div class="source-meta">Relevance: {relevance:.1f} • Source: Papers with Code</div>
                </div>
                '''
            sources_html += '</div>'
        
        # News Articles
        if news_data:
            sources_html += '<div class="source-group">'
            sources_html += '<h4>📰 News Articles</h4>'
            
            for article in news_data[:8]:  # Show top 8
                article_title = self._truncate_text(article.get('title', 'Unknown article'), 100)
                article_url = article.get('url', '#')
                source = article.get('source', 'Unknown')
                relevance = article.get('relevance_score', 0)
                sources_html += f'''
                <div class="source-item">
                    <a href="{article_url}" target="_blank">{article_title}</a>
                    <div class="source-meta">Source: {source} • Relevance: {relevance:.1f}</div>
                </div>
                '''
            sources_html += '</div>'
        
        sources_html += '</div>'
        return sources_html
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to specified length"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def _create_fallback_content(self) -> str:
        """Create simple fallback content if email generation fails"""
        current_date = datetime.now().strftime("%B %d, %Y")
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AI Intelligence Digest - {current_date}</title>
</head>
<body>
    <h1>AI & Robotics Intelligence Digest</h1>
    <p><strong>Date:</strong> {current_date}</p>
    <p><strong>Status:</strong> Email generation encountered an error. Please check the system logs for details.</p>
</body>
</html>
        """

    def _get_better_topic_heading(self, cluster_id: str, cluster_info: Dict) -> str:
        """Generate better, more descriptive topic headings"""
        topic_headings = {
            'openai': '🧠 OpenAI: Privacy, Integrations, and Reasoning Advances',
            'deepmind': '🔬 DeepMind & Google AI: Research Breakthroughs',
            'humanoids': '🤖 Humanoids & Physical AI: Embodied Intelligence',
            'tesla_nvidia': '🚗 Tesla & NVIDIA: Autonomous Systems and AI Hardware',
            'anthropic': '🤝 Anthropic: Claude Safety and Constitutional AI',
            'regulation_ethics': '⚖️ AI Regulation & Ethics: Policy and Safety',
            'research_models': '📚 Foundation Models: LLM Research and Development',
            'robotics_automation': '🏭 Robotics & Automation: Industrial Applications',
            'other': '💡 Emerging AI Developments'
        }
        
        return topic_headings.get(cluster_id, cluster_info.get('display_name', '📊 AI Updates'))
    
    def _generate_executive_summary(self, all_clusters: Dict) -> str:
        """Generate dynamic GPT-powered executive summary from actual cluster data"""
        if not all_clusters:
            return ""
        
        # Get top 3 most active clusters with actual data
        sorted_clusters = sorted(
            all_clusters.items(),
            key=lambda x: sum(1 for v in [x[1]['github'], x[1]['papers'], x[1]['news']] if v is not None),
            reverse=True
        )[:3]
        
        # Prepare cluster data for GPT analysis
        cluster_summaries = {}
        for cluster_id, cluster_data in sorted_clusters:
            cluster_info = {
                'topic': self._get_better_topic_heading(cluster_id, cluster_data['info']),
                'github_activity': cluster_data['github']['analysis'] if cluster_data['github'] else None,
                'research_activity': cluster_data['papers']['analysis'] if cluster_data['papers'] else None,
                'news_activity': cluster_data['news']['analysis'] if cluster_data['news'] else None,
                'source_count': sum(1 for v in [cluster_data['github'], cluster_data['papers'], cluster_data['news']] if v is not None)
            }
            cluster_summaries[cluster_id] = cluster_info
        
        if not cluster_summaries:
            return ""
        
        try:
            from openai import OpenAI
            from config import OPENAI_API_KEY
            
            client = OpenAI(api_key=OPENAI_API_KEY)
            
            prompt = f"""
            Create a concise executive summary from today's AI and robotics intelligence:
            
            Top Active Areas: {json.dumps(cluster_summaries, indent=2)}
            
            Write 2-3 sentences highlighting the most significant developments across these areas. Focus on concrete developments and their implications. Use a professional, analytical tone without markdown formatting.
            
            Example style: "Today's intelligence reveals significant activity in three key areas. OpenAI developments show continued focus on privacy and integration capabilities, while robotics research demonstrates advances in embodied AI systems. The convergence of these trends suggests accelerating deployment of AI in physical applications."
            
            Do not use bullet points, bold text, or section headers.
            """
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.3
            )
            
            summary_text = response.choices[0].message.content.strip()
            
            # Build HTML with GPT-generated summary
            summary_html = f"""
            <div class="executive-summary">
                <h2>📋 Executive Summary</h2>
                <div class="summary-content">
                    <p>{summary_text}</p>
                    
                    <div class="summary-bullets">
            """
            
            # Add activity indicators for top topics
            for cluster_id, cluster_data in sorted_clusters:
                heading = self._get_better_topic_heading(cluster_id, cluster_data['info'])
                source_types = []
                if cluster_data['github']: source_types.append('development')
                if cluster_data['papers']: source_types.append('research')
                if cluster_data['news']: source_types.append('industry news')
                
                topic_name = heading.split(': ')[1] if ': ' in heading else heading.replace('🧠 ', '').replace('🔬 ', '').replace('🤖 ', '').replace('🚗 ', '').replace('🤝 ', '').replace('⚖️ ', '').replace('📚 ', '').replace('🏭 ', '').replace('💡 ', '')
                
                summary_html += f"""
                        <div class="summary-bullet">• <strong>{topic_name}</strong> — Active in {', '.join(source_types)}</div>
                """
            
            summary_html += """
                    </div>
                </div>
            </div>
            """
            
            return summary_html
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            # Minimal fallback without hardcoded content
            return f"""
            <div class="executive-summary">
                <h2>📋 Executive Summary</h2>
                <div class="summary-content">
                    <p>Today's intelligence covers {len(all_clusters)} key topic areas with activity across multiple sources.</p>
                </div>
            </div>
            """

# Legacy EmailAgent for backwards compatibility
class EmailAgent(IntelligentEmailAgent):
    """Backwards compatible wrapper"""
    
    def create_email_content_with_sources(self, 
                                         github_summary: str, 
                                         papers_summary: str, 
                                         news_summary: str, 
                                         strategic_insights: str,
                                         github_data: Dict,
                                         papers_data: List,
                                         news_data: List) -> str:
        """Legacy method - creates basic content"""
        # Create mock digest data for compatibility
        digest_data = {
            'strategic_insights': strategic_insights,
            'github_analysis': {'status': 'success', 'clusters': {}},
            'papers_analysis': {'status': 'success', 'clusters': {}},
            'news_analysis': {'status': 'success', 'clusters': {}}
        }
        
        return self.create_intelligent_email_content(digest_data, github_data, papers_data, news_data)

if __name__ == "__main__":
    # Test the intelligent email agent
    agent = IntelligentEmailAgent()
    
    # Mock test data
    test_digest_data = {
        'strategic_insights': '**Key Trends**: AI development is accelerating across multiple fronts.',
        'github_analysis': {'status': 'success', 'clusters': {}},
        'papers_analysis': {'status': 'no_data', 'message': 'No papers found.'},
        'news_analysis': {'status': 'success', 'clusters': {}}
    }
    
    result = agent.create_intelligent_email_content(test_digest_data, {}, [], [])
    print("📧 Email template generated successfully")
    print(f"Length: {len(result)} characters") 