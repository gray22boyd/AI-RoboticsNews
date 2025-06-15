#!/usr/bin/env python3
"""
Enhanced Email Agent for AI & Robotics Intelligence Digest
Features: Visual hierarchy, actionable insights, trend indicators, and premium design
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import re
import json
from openai import OpenAI
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

class EnhancedEmailAgent:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Activity level thresholds
        self.activity_thresholds = {
            'high': {'github': 8, 'papers': 4, 'news': 6},
            'medium': {'github': 4, 'papers': 2, 'news': 3},
            'low': {'github': 1, 'papers': 1, 'news': 1}
        }
        
        # Urgency indicators
        self.urgency_keywords = {
            'breaking': ['breaking', 'urgent', 'critical', 'emergency', 'immediate'],
            'high': ['major', 'significant', 'important', 'breakthrough', 'milestone'],
            'medium': ['notable', 'interesting', 'development', 'update', 'progress'],
            'low': ['minor', 'small', 'routine', 'maintenance', 'patch']
        }
    
    def create_enhanced_email_content(self, 
                                    digest_data: Dict[str, Any],
                                    github_data: Dict,
                                    papers_data: List,
                                    news_data: List) -> str:
        """Create enhanced email with visual hierarchy and actionable insights"""
        try:
            # CRITICAL FIX: Check for empty data at the start
            total_content = len(github_data.get('commits', [])) + len(papers_data) + len(news_data)
            logger.info(f"📊 Email content check: {total_content} total items to process")
            
            if total_content == 0:
                logger.error("❌ EMERGENCY: No real data available for email content!")
                logger.error("❌ REFUSING to create email with fake data - fix data collection!")
                raise ValueError("No real data available - data collection systems are failing")
            
            current_date = datetime.now().strftime("%B %d, %Y")
            
            # Extract analysis data
            github_analysis = digest_data.get('github_analysis', {})
            papers_analysis = digest_data.get('papers_analysis', {})
            news_analysis = digest_data.get('news_analysis', {})
            strategic_insights = digest_data.get('strategic_insights', '')
            
            # Collect and enrich clusters
            all_clusters = self._collect_and_enrich_clusters(
                github_analysis, papers_analysis, news_analysis
            )
            
            # Generate enhanced content sections
            executive_summary = self._generate_enhanced_executive_summary(all_clusters)
            key_insights = self._generate_key_insights(all_clusters)
            cluster_content = self._build_enhanced_cluster_content(all_clusters)
            action_items = self._generate_action_items(all_clusters)
            strategic_section = self._build_enhanced_strategic_section(strategic_insights)
            sources_section = self._build_enhanced_sources_section(github_data, papers_data, news_data)
            
            # Build complete HTML email
            html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI & Robotics Intelligence Digest</title>
    {self._get_enhanced_styles()}
</head>
<body>
    <div class="email-container">
        {self._build_header(current_date)}
        
        <div class="content-wrapper">
            {executive_summary}
            {key_insights}
            {cluster_content}
            {action_items}
            {strategic_section}
            {sources_section}
        </div>
        
        {self._build_footer()}
    </div>
</body>
</html>
            """
            
            return html_template
            
        except Exception as e:
            logger.error(f"Error creating enhanced email content: {e}")
            return self._create_fallback_content()
    
    def _get_enhanced_styles(self) -> str:
        """Enhanced CSS with modern design, visual hierarchy, and interactive elements"""
        return """
    <style>
        /* Reset and Base Styles */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #1a202c;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        
        .email-container {
            max-width: 900px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        /* Header Styles */
        .header {
            background: linear-gradient(135deg, #1a365d 0%, #2d3748 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
            position: relative;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.3;
        }
        
        .header-content {
            position: relative;
            z-index: 1;
        }
        
        .header h1 {
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }
        
        .header .date {
            font-size: 16px;
            opacity: 0.9;
            font-weight: 500;
        }
        
        .header .digest-stats {
            margin-top: 20px;
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 24px;
            font-weight: 700;
            display: block;
        }
        
        .stat-label {
            font-size: 12px;
            opacity: 0.8;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Content Wrapper */
        .content-wrapper {
            padding: 0;
        }
        
        /* Executive Summary */
        .executive-summary {
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            padding: 40px 30px;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .section-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .section-icon {
            font-size: 24px;
            margin-right: 12px;
        }
        
        .section-title {
            font-size: 24px;
            font-weight: 700;
            color: #2d3748;
            margin: 0;
        }
        
        .summary-content {
            font-size: 18px;
            line-height: 1.7;
            color: #4a5568;
            margin-bottom: 25px;
        }
        
        /* Key Insights Cards */
        .key-insights {
            padding: 40px 30px;
            background: #ffffff;
        }
        
        .insights-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .insight-card {
            background: #f8fafc;
            border-radius: 12px;
            padding: 20px;
            border-left: 4px solid #4299e1;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .insight-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        
        .insight-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
        }
        
        .insight-topic {
            font-weight: 600;
            color: #2d3748;
            font-size: 16px;
        }
        
        .activity-badge {
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .activity-high {
            background: #c6f6d5;
            color: #22543d;
        }
        
        .activity-medium {
            background: #fef5e7;
            color: #c05621;
        }
        
        .activity-low {
            background: #e2e8f0;
            color: #4a5568;
        }
        
        .trend-indicator {
            font-size: 18px;
            margin-left: 8px;
        }
        
        .insight-summary {
            font-size: 14px;
            line-height: 1.5;
            color: #718096;
        }
        
        /* Topic Clusters */
        .topic-clusters {
            background: #ffffff;
        }
        
        .cluster-section {
            border-bottom: 1px solid #f1f5f9;
            padding: 40px 30px;
        }
        
        .cluster-section:last-child {
            border-bottom: none;
        }
        
        .cluster-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 25px;
        }
        
        .cluster-title {
            font-size: 22px;
            font-weight: 700;
            color: #2d3748;
            display: flex;
            align-items: center;
        }
        
        .cluster-meta {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .urgency-indicator {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .urgency-breaking {
            background: #fed7d7;
            color: #c53030;
            animation: pulse 2s infinite;
        }
        
        .urgency-high {
            background: #fef5e7;
            color: #c05621;
        }
        
        .urgency-medium {
            background: #e6fffa;
            color: #234e52;
        }
        
        .urgency-low {
            background: #f0f4f8;
            color: #4a5568;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .subsection-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .subsection {
            background: #f8fafc;
            border-radius: 12px;
            padding: 20px;
            border-left: 4px solid #cbd5e0;
        }
        
        .subsection.github {
            border-left-color: #48bb78;
            background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
        }
        
        .subsection.papers {
            border-left-color: #ed8936;
            background: linear-gradient(135deg, #fffaf0 0%, #fbd38d 100%);
        }
        
        .subsection.news {
            border-left-color: #4299e1;
            background: linear-gradient(135deg, #ebf8ff 0%, #90cdf4 100%);
        }
        
        .subsection-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 15px;
        }
        
        .subsection-title {
            font-weight: 600;
            color: #2d3748;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .source-count {
            background: rgba(255,255,255,0.8);
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            color: #4a5568;
        }
        
        .analysis-content {
            font-size: 15px;
            line-height: 1.6;
            color: #4a5568;
        }
        
        /* Action Items */
        .action-items {
            background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
            color: white;
            padding: 40px 30px;
        }
        
        .action-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 25px;
        }
        
        .action-card {
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        .action-type {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            opacity: 0.8;
            margin-bottom: 8px;
        }
        
        .action-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        
        .action-description {
            font-size: 14px;
            line-height: 1.5;
            opacity: 0.9;
        }
        
        /* Strategic Section */
        .strategic-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 12px;
            margin: 30px 0;
            border: 1px solid rgba(255,255,255,0.1);
            overflow: hidden; /* Prevent text overflow */
        }

        .strategic-section .section-header h2 {
            margin-top: 0;
            margin-bottom: 15px;
            font-size: 20px;
            color: white;
            font-weight: 700;
            text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        }

        .strategic-content {
            color: white;
            font-size: 16px;
            line-height: 1.7;
            font-weight: 400;
            text-shadow: 0 1px 2px rgba(0,0,0,0.2);
            word-wrap: break-word; /* Handle long words */
        }

        .strategic-content strong {
            color: #fff;
            font-weight: 600;
        }
        
        /* Sources Section */
        .sources-section {
            background: #f8fafc;
            padding: 40px 30px;
        }
        
        .sources-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 25px;
        }
        
        .source-group {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .source-group h4 {
            font-size: 16px;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        
        .source-group h4::before {
            content: '';
            width: 4px;
            height: 20px;
            background: #4299e1;
            border-radius: 2px;
            margin-right: 10px;
        }
        
        .source-item {
            padding: 12px 0;
            border-bottom: 1px solid #f1f5f9;
        }
        
        .source-item:last-child {
            border-bottom: none;
        }
        
        .source-item a {
            color: #4299e1;
            text-decoration: none;
            font-weight: 500;
            font-size: 14px;
            line-height: 1.4;
        }
        
        .source-item a:hover {
            text-decoration: underline;
        }
        
        .source-meta {
            font-size: 12px;
            color: #718096;
            margin-top: 4px;
        }
        
        /* Footer */
        .footer {
            background: #2d3748;
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .footer-content {
            font-size: 14px;
            opacity: 0.8;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .email-container {
                margin: 10px;
                border-radius: 12px;
            }
            
            .header {
                padding: 30px 20px;
            }
            
            .header h1 {
                font-size: 24px;
            }
            
            .content-wrapper {
                padding: 0;
            }
            
            .executive-summary,
            .key-insights,
            .cluster-section,
            .action-items,
            .strategic-section,
            .sources-section {
                padding: 30px 20px;
            }
            
            .insights-grid,
            .subsection-grid,
            .action-grid,
            .sources-grid {
                grid-template-columns: 1fr;
            }
            
            .digest-stats {
                gap: 20px !important;
            }
        }
    </style>
        """
    
    def _build_header(self, current_date: str) -> str:
        """Build enhanced header with statistics"""
        return f"""
        <div class="header">
            <div class="header-content">
                <h1>AI & Robotics Intelligence Digest</h1>
                <div class="date">{current_date}</div>
                <div class="digest-stats">
                    <div class="stat-item">
                        <span class="stat-number" id="github-count">-</span>
                        <span class="stat-label">Commits</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number" id="papers-count">-</span>
                        <span class="stat-label">Papers</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number" id="news-count">-</span>
                        <span class="stat-label">Articles</span>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def _build_footer(self) -> str:
        """Build footer section"""
        return """
        <div class="footer">
            <div class="footer-content">
                <p>AI & Robotics Intelligence Digest • Powered by GPT-4 Analysis</p>
                <p style="margin-top: 8px; font-size: 12px;">
                    This digest uses intelligent clustering and analysis to provide actionable insights from GitHub, research papers, and industry news.
                </p>
            </div>
        </div>
        """

    def _collect_and_enrich_clusters(self, github_analysis: Dict, papers_analysis: Dict, news_analysis: Dict) -> Dict:
        """Collect and enrich clusters with activity levels and trends"""
        all_clusters = {}
        
        # Collect clusters from all sources
        for analysis_type, analysis_data in [
            ('github', github_analysis),
            ('papers', papers_analysis), 
            ('news', news_analysis)
        ]:
            if analysis_data.get('status') == 'success':
                for cluster_id, cluster_data in analysis_data.get('clusters', {}).items():
                    if cluster_id not in all_clusters:
                        all_clusters[cluster_id] = {
                            'info': cluster_data['cluster_info'],
                            'github': None,
                            'papers': None,
                            'news': None,
                            'activity_level': 'low',
                            'trend': 'stable',
                            'urgency': 'low'
                        }
                    
                    all_clusters[cluster_id][analysis_type] = cluster_data
        
        # Enrich with activity levels and trends
        for cluster_id, cluster_data in all_clusters.items():
            cluster_data['activity_level'] = self._calculate_activity_level(cluster_data)
            cluster_data['trend'] = self._determine_trend(cluster_data)
            cluster_data['urgency'] = self._assess_urgency(cluster_data)
        
        # If no clusters found, log the issue but don't create fake data
        if not all_clusters:
            logger.error("❌ NO REAL CLUSTERS FOUND - Data collection is failing!")
            logger.error("❌ This indicates the monitoring systems are not collecting real data")
        
        return all_clusters
    
    def _calculate_activity_level(self, cluster_data: Dict) -> str:
        """Calculate activity level based on source counts"""
        github_count = cluster_data.get('github', {}).get('commit_count', 0) if cluster_data.get('github') else 0
        papers_count = cluster_data.get('papers', {}).get('paper_count', 0) if cluster_data.get('papers') else 0
        news_count = cluster_data.get('news', {}).get('article_count', 0) if cluster_data.get('news') else 0
        
        if (github_count >= self.activity_thresholds['high']['github'] or 
            papers_count >= self.activity_thresholds['high']['papers'] or 
            news_count >= self.activity_thresholds['high']['news']):
            return 'high'
        elif (github_count >= self.activity_thresholds['medium']['github'] or 
              papers_count >= self.activity_thresholds['medium']['papers'] or 
              news_count >= self.activity_thresholds['medium']['news']):
            return 'medium'
        else:
            return 'low'
    
    def _determine_trend(self, cluster_data: Dict) -> str:
        """Determine trend direction based on content analysis"""
        # Analyze content for trend indicators
        all_text = ""
        for source in ['github', 'papers', 'news']:
            if cluster_data.get(source):
                all_text += cluster_data[source].get('analysis', '') + " "
        
        all_text = all_text.lower()
        
        # Trend keywords
        increasing_keywords = ['growing', 'increasing', 'expanding', 'rising', 'surge', 'boom', 'accelerating']
        decreasing_keywords = ['declining', 'decreasing', 'falling', 'dropping', 'slowing', 'reducing']
        
        increasing_count = sum(1 for keyword in increasing_keywords if keyword in all_text)
        decreasing_count = sum(1 for keyword in decreasing_keywords if keyword in all_text)
        
        if increasing_count > decreasing_count:
            return 'increasing'
        elif decreasing_count > increasing_count:
            return 'decreasing'
        else:
            return 'stable'
    
    def _assess_urgency(self, cluster_data: Dict) -> str:
        """Assess urgency level based on content keywords"""
        all_text = ""
        for source in ['github', 'papers', 'news']:
            if cluster_data.get(source):
                all_text += cluster_data[source].get('analysis', '') + " "
        
        all_text = all_text.lower()
        
        for urgency_level, keywords in self.urgency_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                return urgency_level
        
        return 'low'
    
    def _generate_enhanced_executive_summary(self, all_clusters: Dict) -> str:
        """Generate enhanced executive summary with GPT analysis"""
        if not all_clusters:
            return ""
        
        # Get top 3 most active clusters
        sorted_clusters = sorted(
            all_clusters.items(),
            key=lambda x: (
                x[1]['activity_level'] == 'high',
                x[1]['activity_level'] == 'medium',
                sum(1 for v in [x[1].get('github'), x[1].get('papers'), x[1].get('news')] if v is not None)
            ),
            reverse=True
        )[:3]
        
        try:
            # Prepare cluster data for GPT
            cluster_summaries = {}
            for cluster_id, cluster_data in sorted_clusters:
                cluster_summaries[cluster_id] = {
                    'topic': cluster_data['info'].get('display_name', cluster_id),
                    'activity_level': cluster_data['activity_level'],
                    'trend': cluster_data['trend'],
                    'urgency': cluster_data['urgency'],
                    'sources': [k for k in ['github', 'papers', 'news'] if cluster_data.get(k)]
                }
            
            prompt = f"""
            You are a strategic intelligence analyst. Write exactly 2-3 sentences that answer: "What are the most important AI developments today and what specific actions should leaders take?"

            Data: {json.dumps(cluster_summaries, indent=2)}

            STRICT REQUIREMENTS:
            - Maximum 3 sentences, minimum 2 sentences
            - Each sentence must mention SPECIFIC companies, technologies, or numbers
            - Each sentence must end with a CONCRETE action (not "consider" or "align")
            - NO generic terms: avoid "robust", "stable growth", "opportunities", "strategies"
            - NO vague actions: avoid "consider partnerships", "align strategies", "integrate technologies"

            REQUIRED FORMAT for each sentence:
            [Specific development with companies/numbers] → [Clear implication] → [Concrete action verb + specific target]

            GOOD EXAMPLES:
            "NVIDIA's European expansion through new developer tools and Training Cluster as a Service partnership with Hugging Face signals a push toward regional AI sovereignty. Organizations should audit their AI vendor dependencies and establish European data processing capabilities by Q3 2025."

            "OpenAI's legal battle with The New York Times over indefinite data retention coincides with humanoid robotics safety discussions, indicating regulatory pressure will accelerate across AI sectors. Companies should implement data minimization policies and begin robotics safety compliance frameworks immediately."

            BAD EXAMPLES (don't write like this):
            "Foundation models are seeing robust growth. Leaders should align their strategies accordingly."
            "AI developments suggest opportunities. Companies should consider partnerships."
            "The landscape shows stable trends with potential for innovation."

            FORBIDDEN WORDS: robust, stable, growth, opportunities, strategies, accordingly, potential, developments, advancements, landscape, trends (unless referring to specific market trends with numbers)

            REQUIRED WORDS: Must include at least 2 company names, at least 1 specific technology/product, at least 1 concrete timeline or number.

            Write exactly 2-3 sentences. No quotes around the text. No introductory phrases.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=120,  # Reduced from 200 to force conciseness
                temperature=0.2  # Lower temperature for more focused output
            )
            
            summary_text = response.choices[0].message.content.strip()
            
            # Ensure complete sentences (basic validation)
            if not summary_text.endswith('.'):
                summary_text += '.'
            
            return f"""
            <div class="executive-summary">
                <div class="section-header">
                    <span class="section-icon">📋</span>
                    <h2 class="section-title">Executive Summary</h2>
                </div>
                <div class="summary-content">
                    {summary_text}
                </div>
            </div>
            """
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            # More specific fallback based on actual data
            high_activity_areas = [
                cluster_data['info'].get('display_name', cluster_id) 
                for cluster_id, cluster_data in all_clusters.items() 
                if cluster_data.get('activity_level') == 'high'
            ][:2]
            
            if high_activity_areas:
                fallback_text = f"Today's intelligence highlights significant activity in {' and '.join(high_activity_areas)} with {len(all_clusters)} total areas monitored."
            else:
                fallback_text = f"Today's intelligence covers {len(all_clusters)} key areas with significant activity in foundation models and autonomous systems development."
            
            return f"""
            <div class="executive-summary">
                <div class="section-header">
                    <span class="section-icon">📋</span>
                    <h2 class="section-title">Executive Summary</h2>
                </div>
                <div class="summary-content">
                    <p>{fallback_text}</p>
                </div>
            </div>
            """
    
    def _generate_key_insights(self, all_clusters: Dict) -> str:
        """Generate key insights cards with visual indicators"""
        if not all_clusters:
            return ""
        
        insights_html = """
        <div class="key-insights">
            <div class="section-header">
                <span class="section-icon">💡</span>
                <h2 class="section-title">Key Insights</h2>
            </div>
            <div class="insights-grid">
        """
        
        # Sort clusters by activity and show top 6
        sorted_clusters = sorted(
            all_clusters.items(),
            key=lambda x: (
                x[1]['activity_level'] == 'high',
                x[1]['activity_level'] == 'medium',
                sum(1 for v in [x[1].get('github'), x[1].get('papers'), x[1].get('news')] if v is not None)
            ),
            reverse=True
        )[:6]
        
        for cluster_id, cluster_data in sorted_clusters:
            topic_name = cluster_data['info'].get('display_name', cluster_id)
            activity_level = cluster_data['activity_level']
            trend = cluster_data['trend']
            
            # Get trend arrow
            trend_arrows = {
                'increasing': '↗️',
                'decreasing': '↘️',
                'stable': '➡️'
            }
            trend_arrow = trend_arrows.get(trend, '➡️')
            
            # Generate brief insight
            sources = [k for k in ['github', 'papers', 'news'] if cluster_data.get(k)]
            source_text = ', '.join(sources)
            
            insights_html += f"""
            <div class="insight-card">
                <div class="insight-header">
                    <div class="insight-topic">{topic_name}</div>
                    <div>
                        <span class="activity-badge activity-{activity_level}">{activity_level}</span>
                        <span class="trend-indicator">{trend_arrow}</span>
                    </div>
                </div>
                <div class="insight-summary">
                    Active in {source_text}. Trend: {trend} activity with {activity_level} priority level.
                </div>
            </div>
            """
        
        insights_html += """
            </div>
        </div>
        """
        
        return insights_html
    
    def _build_enhanced_cluster_content(self, all_clusters: Dict) -> str:
        """Build enhanced cluster content with visual hierarchy"""
        if not all_clusters:
            return self._build_no_data_message()
        
        content_html = '<div class="topic-clusters">'
        
        # Sort clusters by priority
        sorted_clusters = sorted(
            all_clusters.items(),
            key=lambda x: (
                x[1]['urgency'] == 'breaking',
                x[1]['urgency'] == 'high',
                x[1]['activity_level'] == 'high',
                x[1]['activity_level'] == 'medium',
                sum(1 for v in [x[1].get('github'), x[1].get('papers'), x[1].get('news')] if v is not None)
            ),
            reverse=True
        )
        
        for cluster_id, cluster_data in sorted_clusters:
            cluster_info = cluster_data['info']
            topic_name = cluster_info.get('display_name', cluster_id)
            
            content_html += f"""
            <div class="cluster-section">
                <div class="cluster-header">
                    <h3 class="cluster-title">{topic_name}</h3>
                    <div class="cluster-meta">
                        <span class="urgency-indicator urgency-{cluster_data['urgency']}">{cluster_data['urgency']}</span>
                        <span class="activity-badge activity-{cluster_data['activity_level']}">{cluster_data['activity_level']}</span>
                    </div>
                </div>
                
                <div class="subsection-grid">
            """
            
            # Add subsections for each data source
            for source_type, source_key in [('🔧 Development', 'github'), ('📚 Research', 'papers'), ('📡 Industry News', 'news')]:
                if cluster_data.get(source_key):
                    source_data = cluster_data[source_key]
                    count_key = {'github': 'commit_count', 'papers': 'paper_count', 'news': 'article_count'}[source_key]
                    count = source_data.get(count_key, 0)
                    
                    content_html += f"""
                    <div class="subsection {source_key}">
                        <div class="subsection-header">
                            <div class="subsection-title">{source_type}</div>
                            <div class="source-count">{count} items</div>
                        </div>
                        <div class="analysis-content">{source_data.get('analysis', '')}</div>
                    </div>
                    """
            
            content_html += """
                </div>
            </div>
            """
        
        content_html += '</div>'
        return content_html
    
    def _generate_action_items(self, all_clusters: Dict) -> str:
        """Generate actionable insights and recommendations"""
        if not all_clusters:
            return ""
        
        try:
            # Get high-priority clusters
            high_priority_clusters = [
                (cluster_id, cluster_data) for cluster_id, cluster_data in all_clusters.items()
                if cluster_data['urgency'] in ['breaking', 'high'] or cluster_data['activity_level'] == 'high'
            ]
            
            if not high_priority_clusters:
                return ""
            
            # Generate action items with GPT
            cluster_info = {}
            for cluster_id, cluster_data in high_priority_clusters[:4]:  # Top 4
                cluster_info[cluster_id] = {
                    'topic': cluster_data['info'].get('display_name', cluster_id),
                    'urgency': cluster_data['urgency'],
                    'activity_level': cluster_data['activity_level'],
                    'sources': [k for k in ['github', 'papers', 'news'] if cluster_data.get(k)]
                }
            
            prompt = f"""
            Generate 3-4 specific action items based on these high-priority AI developments:
            
            {json.dumps(cluster_info, indent=2)}
            
            For each action item, provide:
            1. Action type (Monitor, Investigate, Evaluate, or Prepare)
            2. Specific action title (max 8 words)
            3. Brief description (1-2 sentences)
            
            Focus on actionable business/technical decisions. Format as JSON array:
            [{"type": "Monitor", "title": "Track OpenAI API Changes", "description": "..."}]
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.4
            )
            
            try:
                response_text = response.choices[0].message.content.strip()
                # Clean up response if it contains extra text
                if '[' in response_text and ']' in response_text:
                    start = response_text.find('[')
                    end = response_text.rfind(']') + 1
                    response_text = response_text[start:end]
                actions = json.loads(response_text)
            except Exception as e:
                logger.warning(f"JSON parsing failed for action items: {e}")
                # Fallback if JSON parsing fails
                actions = [
                    {"type": "Monitor", "title": "Track High-Priority Developments", "description": "Continue monitoring the identified high-activity areas for strategic implications."},
                    {"type": "Evaluate", "title": "Assess Competitive Impact", "description": "Evaluate how these developments might affect competitive positioning."}
                ]
            
            action_html = """
            <div class="action-items">
                <div class="section-header">
                    <span class="section-icon">🎯</span>
                    <h2 class="section-title">Recommended Actions</h2>
                </div>
                <div class="action-grid">
            """
            
            for action in actions[:4]:  # Max 4 actions
                action_html += f"""
                <div class="action-card">
                    <div class="action-type">{action.get('type', 'Action')}</div>
                    <div class="action-title">{action.get('title', 'Review Developments')}</div>
                    <div class="action-description">{action.get('description', 'Monitor ongoing developments in this area.')}</div>
                </div>
                """
            
            action_html += """
                </div>
            </div>
            """
            
            return action_html
            
        except Exception as e:
            logger.error(f"Error generating action items: {e}")
            return ""
    
    def _build_enhanced_strategic_section(self, strategic_insights: str) -> str:
        """Build strategic insights section with readable styling"""
        if not strategic_insights or strategic_insights.strip() == "":
            return ""
        
        return f"""
        <div class="strategic-section">
            <div class="section-header">
                <span class="section-icon">🧠</span>
                <h2 class="section-title">Strategic Intelligence</h2>
            </div>
            <div class="strategic-content">{strategic_insights}</div>
        </div>
        """
    
    def _build_enhanced_sources_section(self, github_data: Dict, papers_data: List, news_data: List) -> str:
        """Build enhanced sources section with better organization"""
        sources_html = """
        <div class="sources-section">
            <div class="section-header">
                <span class="section-icon">📚</span>
                <h2 class="section-title">Sources & References</h2>
            </div>
            <div class="sources-grid">
        """
        
        # GitHub Sources
        commits = github_data.get('commits', [])
        if commits:
            sources_html += """
            <div class="source-group">
                <h4>🔧 Development Activity</h4>
            """
            
            for commit in commits[:6]:  # Show top 6
                commit_title = self._truncate_text(commit.get('message', 'Unknown commit'), 60)
                commit_url = commit.get('url', '#')
                repo = commit.get('repo', 'unknown')
                author = commit.get('author', 'unknown')
                
                sources_html += f"""
                <div class="source-item">
                    <a href="{commit_url}" target="_blank">{repo}: {commit_title}</a>
                    <div class="source-meta">by {author} • {commit.get('sha', '')[:8]}</div>
                </div>
                """
            
            sources_html += '</div>'
        
        # Research Papers
        if papers_data:
            sources_html += """
            <div class="source-group">
                <h4>📚 Research Papers</h4>
            """
            
            for paper in papers_data[:5]:  # Show top 5
                paper_title = self._truncate_text(paper.get('title', 'Unknown paper'), 80)
                paper_url = paper.get('url', '#')
                relevance = paper.get('relevance_score', 0)
                
                sources_html += f"""
                <div class="source-item">
                    <a href="{paper_url}" target="_blank">{paper_title}</a>
                    <div class="source-meta">Relevance: {relevance:.1f}/10 • Papers with Code</div>
                </div>
                """
            
            sources_html += '</div>'
        
        # News Articles
        if news_data:
            sources_html += """
            <div class="source-group">
                <h4>📰 Industry News</h4>
            """
            
            for article in news_data[:6]:  # Show top 6
                article_title = self._truncate_text(article.get('title', 'Unknown article'), 80)
                article_url = article.get('url', '#')
                source = article.get('source', 'Unknown')
                
                sources_html += f"""
                <div class="source-item">
                    <a href="{article_url}" target="_blank">{article_title}</a>
                    <div class="source-meta">Source: {source}</div>
                </div>
                """
            
            sources_html += '</div>'
        
        sources_html += """
            </div>
        </div>
        """
        
        return sources_html
    
    def _build_no_data_message(self) -> str:
        """Build enhanced no data message"""
        return """
        <div class="topic-clusters">
            <div class="cluster-section">
                <div style="text-align: center; padding: 40px 20px; color: #718096;">
                    <h3 style="margin-bottom: 15px;">📊 Limited Intelligence Available</h3>
                    <p>No significant topic clusters were identified across GitHub, research papers, and news sources during this monitoring period.</p>
                    <p style="margin-top: 10px; font-size: 14px;">This may indicate a quieter day in AI/robotics developments or suggest expanding monitoring sources.</p>
                </div>
            </div>
        </div>
        """
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to specified length"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def _create_fallback_content(self) -> str:
        """Create enhanced fallback content"""
        current_date = datetime.now().strftime("%B %d, %Y")
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Intelligence Digest - {current_date}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 40px; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 40px; background: #f8fafc; border-radius: 12px; }}
        h1 {{ color: #2d3748; margin-bottom: 20px; }}
        .error {{ background: #fed7d7; color: #c53030; padding: 20px; border-radius: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>AI & Robotics Intelligence Digest</h1>
        <p><strong>Date:</strong> {current_date}</p>
        <div class="error">
            <strong>System Notice:</strong> Email generation encountered an error. Please check system logs and try again.
        </div>
    </div>
</body>
</html>
                """
    
    def _create_no_data_email(self) -> str:
        """Create a complete email when no data is available"""
        current_date = datetime.now().strftime("%B %d, %Y")
        
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI & Robotics Intelligence Digest - Service Notice</title>
    {self._get_enhanced_styles()}
</head>
<body>
    <div class="email-container">
        {self._build_header(current_date)}
        
        <div class="content-wrapper">
            <div class="executive-summary">
                <div class="section-header">
                    <span class="section-icon">🔧</span>
                    <h2 class="section-title">Data Collection Notice</h2>
                </div>
                <div class="summary-content">
                    <p>Our AI monitoring systems are currently experiencing data collection issues. This may be due to:</p>
                    <ul>
                        <li>API rate limiting or temporary service outages</li>
                        <li>Overly restrictive content filtering thresholds</li>
                        <li>Network connectivity issues</li>
                    </ul>
                    <p>Our technical team has been notified and is working to resolve these issues. You should receive your next digest with full content tomorrow.</p>
                </div>
            </div>
            
            <div class="key-insights">
                <div class="section-header">
                    <span class="section-icon">⚙️</span>
                    <h2 class="section-title">System Status</h2>
                </div>
                <div class="insights-grid">
                    <div class="insight-card">
                        <div class="insight-header">
                            <div class="insight-topic">GitHub Monitor</div>
                            <span class="activity-badge activity-low">checking</span>
                        </div>
                        <div class="insight-summary">Monitoring AI repository activity across major projects.</div>
                    </div>
                    <div class="insight-card">
                        <div class="insight-header">
                            <div class="insight-topic">Research Papers</div>
                            <span class="activity-badge activity-low">checking</span>
                        </div>
                        <div class="insight-summary">Scanning Papers With Code for latest AI research.</div>
                    </div>
                    <div class="insight-card">
                        <div class="insight-header">
                            <div class="insight-topic">Industry News</div>
                            <span class="activity-badge activity-low">checking</span>
                        </div>
                        <div class="insight-summary">Aggregating AI and robotics news from multiple sources.</div>
                    </div>
                </div>
            </div>
        </div>
        
        {self._build_footer()}
    </div>
</body>
</html>
        """

# Backwards compatibility wrapper
class EmailAgent(EnhancedEmailAgent):
    """Backwards compatible wrapper for existing code"""
    
    def create_email_content_with_sources(self, 
                                         github_summary: str, 
                                         papers_summary: str, 
                                         news_summary: str, 
                                         strategic_insights: str,
                                         github_data: Dict,
                                         papers_data: List,
                                         news_data: List) -> str:
        """Legacy method - creates enhanced content"""
        # Create mock digest data for compatibility
        digest_data = {
            'strategic_insights': strategic_insights,
            'github_analysis': {'status': 'success', 'clusters': {}},
            'papers_analysis': {'status': 'success', 'clusters': {}},
            'news_analysis': {'status': 'success', 'clusters': {}}
        }
        
        return self.create_enhanced_email_content(digest_data, github_data, papers_data, news_data)

if __name__ == "__main__":
    # Test the enhanced email agent
    agent = EnhancedEmailAgent()
    print("🚀 Enhanced Email Agent initialized successfully")
    print("Features: Visual hierarchy, actionable insights, trend indicators, responsive design") 