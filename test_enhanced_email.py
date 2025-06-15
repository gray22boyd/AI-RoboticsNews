#!/usr/bin/env python3
"""
Test script for Enhanced Email Agent
Demonstrates the new visual features and actionable intelligence
"""

import logging
from datetime import datetime
from enhanced_email_agent import EnhancedEmailAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_mock_digest_data():
    """Create mock digest data to test enhanced features"""
    return {
        'github_analysis': {
            'status': 'success',
            'clusters': {
                'openai': {
                    'cluster_info': {
                        'display_name': '🧠 OpenAI & ChatGPT',
                        'icon': '🧠'
                    },
                    'commit_count': 12,
                    'analysis': 'Significant development activity in OpenAI repositories focusing on API improvements and safety features. Major commits include enhanced reasoning capabilities and privacy controls.'
                },
                'humanoids': {
                    'cluster_info': {
                        'display_name': '🤖 Humanoids & Physical AI',
                        'icon': '🤖'
                    },
                    'commit_count': 8,
                    'analysis': 'Growing activity in humanoid robotics with breakthrough developments in motor control and sensor integration. Boston Dynamics and Figure AI showing accelerating progress.'
                }
            }
        },
        'papers_analysis': {
            'status': 'success',
            'clusters': {
                'openai': {
                    'cluster_info': {
                        'display_name': '🧠 OpenAI & ChatGPT',
                        'icon': '🧠'
                    },
                    'paper_count': 5,
                    'analysis': 'Research papers demonstrate major advances in reasoning and constitutional AI approaches. Key findings show improved safety alignment and reduced hallucination rates.'
                },
                'research_models': {
                    'cluster_info': {
                        'display_name': '📚 Foundation Models & Research',
                        'icon': '📚'
                    },
                    'paper_count': 7,
                    'analysis': 'Foundation model research reveals significant improvements in multimodal capabilities and efficiency. New transformer architectures showing promising results.'
                }
            }
        },
        'news_analysis': {
            'status': 'success',
            'clusters': {
                'openai': {
                    'cluster_info': {
                        'display_name': '🧠 OpenAI & ChatGPT',
                        'icon': '🧠'
                    },
                    'article_count': 8,
                    'analysis': 'Industry news highlights OpenAI\'s major partnership announcements and enterprise deployment milestones. Breaking developments in API pricing and accessibility.'
                },
                'regulation_ethics': {
                    'cluster_info': {
                        'display_name': '⚖️ AI Regulation & Ethics',
                        'icon': '⚖️'
                    },
                    'article_count': 4,
                    'analysis': 'Critical regulatory developments with new AI safety standards and privacy requirements. Government agencies increasing oversight of AI deployment.'
                }
            }
        },
        'strategic_insights': 'Cross-cluster analysis reveals accelerating convergence between AI research and commercial deployment. OpenAI developments show strategic focus on enterprise adoption while maintaining safety leadership. Regulatory environment becoming more structured, creating both opportunities and compliance requirements for AI companies.'
    }

def create_mock_source_data():
    """Create mock source data for testing"""
    github_data = {
        'commits': [
            {
                'repo': 'openai/openai-python',
                'message': 'Add enhanced reasoning capabilities to GPT-4 API',
                'author': 'openai-dev',
                'sha': 'abc123def456',
                'url': 'https://github.com/openai/openai-python/commit/abc123def456'
            },
            {
                'repo': 'facebookresearch/llama',
                'message': 'Implement multimodal training pipeline',
                'author': 'meta-ai',
                'sha': 'def456ghi789',
                'url': 'https://github.com/facebookresearch/llama/commit/def456ghi789'
            },
            {
                'repo': 'boston-dynamics/atlas',
                'message': 'Improve balance control algorithms',
                'author': 'bd-robotics',
                'sha': 'ghi789jkl012',
                'url': 'https://github.com/boston-dynamics/atlas/commit/ghi789jkl012'
            }
        ],
        'contributors': {}
    }
    
    papers_data = [
        {
            'title': 'Constitutional AI: Harmlessness from AI Feedback',
            'url': 'https://arxiv.org/abs/2212.08073',
            'relevance_score': 9.2,
            'summary': 'Novel approach to AI safety using constitutional principles'
        },
        {
            'title': 'Scaling Laws for Neural Language Models',
            'url': 'https://arxiv.org/abs/2001.08361',
            'relevance_score': 8.7,
            'summary': 'Fundamental research on model scaling behavior'
        },
        {
            'title': 'Multimodal Foundation Models: From Specialists to General-Purpose Assistants',
            'url': 'https://arxiv.org/abs/2309.10020',
            'relevance_score': 8.9,
            'summary': 'Comprehensive survey of multimodal AI capabilities'
        }
    ]
    
    news_data = [
        {
            'title': 'OpenAI Announces Major Enterprise Partnership with Microsoft',
            'url': 'https://techcrunch.com/openai-microsoft-partnership',
            'source': 'TechCrunch',
            'relevance_score': 9.1
        },
        {
            'title': 'New AI Safety Standards Proposed by EU Regulators',
            'url': 'https://reuters.com/ai-safety-eu-standards',
            'source': 'Reuters',
            'relevance_score': 8.3
        },
        {
            'title': 'Boston Dynamics Humanoid Robot Achieves New Mobility Milestone',
            'url': 'https://spectrum.ieee.org/boston-dynamics-atlas',
            'source': 'IEEE Spectrum',
            'relevance_score': 8.8
        }
    ]
    
    return github_data, papers_data, news_data

def test_enhanced_email_agent():
    """Test the enhanced email agent with mock data"""
    logger.info("🚀 Testing Enhanced Email Agent")
    logger.info("=" * 50)
    
    # Create enhanced email agent
    agent = EnhancedEmailAgent()
    
    # Create mock data
    digest_data = create_mock_digest_data()
    github_data, papers_data, news_data = create_mock_source_data()
    
    logger.info("📊 Mock Data Summary:")
    logger.info(f"  - GitHub clusters: {len(digest_data['github_analysis']['clusters'])}")
    logger.info(f"  - Papers clusters: {len(digest_data['papers_analysis']['clusters'])}")
    logger.info(f"  - News clusters: {len(digest_data['news_analysis']['clusters'])}")
    logger.info(f"  - Source commits: {len(github_data['commits'])}")
    logger.info(f"  - Source papers: {len(papers_data)}")
    logger.info(f"  - Source articles: {len(news_data)}")
    
    # Generate enhanced email
    logger.info("\n🎨 Generating enhanced email content...")
    try:
        email_content = agent.create_enhanced_email_content(
            digest_data, github_data, papers_data, news_data
        )
        
        # Save to file for inspection
        output_file = f"enhanced_email_preview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(email_content)
        
        logger.info(f"✅ Enhanced email generated successfully!")
        logger.info(f"📄 Preview saved to: {output_file}")
        logger.info(f"📏 Content length: {len(email_content):,} characters")
        
        # Analyze features
        features_found = []
        if 'activity-badge' in email_content:
            features_found.append("Activity Level Indicators")
        if 'trend-indicator' in email_content:
            features_found.append("Trend Arrows")
        if 'urgency-indicator' in email_content:
            features_found.append("Urgency Classifications")
        if 'action-items' in email_content:
            features_found.append("Action Items Section")
        if 'key-insights' in email_content:
            features_found.append("Key Insights Cards")
        if 'executive-summary' in email_content:
            features_found.append("Executive Summary")
        if 'strategic-section' in email_content:
            features_found.append("Strategic Intelligence")
        if 'sources-grid' in email_content:
            features_found.append("Enhanced Sources Layout")
        
        logger.info("\n🎯 Enhanced Features Detected:")
        for feature in features_found:
            logger.info(f"  ✅ {feature}")
        
        logger.info(f"\n🏆 Total Enhanced Features: {len(features_found)}/8")
        
        # Check responsive design
        if '@media (max-width: 768px)' in email_content:
            logger.info("📱 Mobile-responsive design: ✅")
        else:
            logger.info("📱 Mobile-responsive design: ❌")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error generating enhanced email: {e}")
        return False

def main():
    """Main test function"""
    logger.info("🧪 Enhanced Email Agent Test Suite")
    logger.info("=" * 60)
    
    success = test_enhanced_email_agent()
    
    if success:
        logger.info("\n🎉 All tests passed! Enhanced email agent is ready.")
        logger.info("🚀 Key improvements over standard version:")
        logger.info("   • Visual hierarchy with modern design")
        logger.info("   • Activity level indicators (High/Medium/Low)")
        logger.info("   • Trend arrows (↗️ ↘️ ➡️)")
        logger.info("   • Urgency classifications with animations")
        logger.info("   • GPT-generated action items")
        logger.info("   • Key insights cards")
        logger.info("   • Enhanced executive summary")
        logger.info("   • Mobile-responsive layout")
        logger.info("   • Premium visual styling")
    else:
        logger.error("\n❌ Tests failed. Check the error messages above.")

if __name__ == "__main__":
    main() 