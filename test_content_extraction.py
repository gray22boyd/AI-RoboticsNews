#!/usr/bin/env python3
"""
Test script for advanced content extraction and analysis
"""

import logging
from summarize_agent import IntelligentSummarizeAgent
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_content_extraction():
    """Test the content extraction functionality"""
    
    agent = IntelligentSummarizeAgent()
    
    # Test articles from reliable sources
    test_articles = [
        {
            'title': 'OpenAI Announces New AI Model',
            'url': 'https://techcrunch.com/2024/12/01/openai-announces-new-ai-model/',
            'source': 'TechCrunch',
            'description': 'OpenAI has announced a new AI model with improved capabilities.',
            'relevance_score': 8.5
        },
        {
            'title': 'NVIDIA Expands AI Infrastructure',
            'url': 'https://www.theverge.com/2024/12/01/nvidia-ai-infrastructure',
            'source': 'The Verge',
            'description': 'NVIDIA announces expansion of AI infrastructure services.',
            'relevance_score': 7.8
        }
    ]
    
    print("🧪 Testing Content Extraction...")
    print("=" * 50)
    
    # Test individual content extraction
    for article in test_articles:
        print(f"\n📄 Testing: {article['title']}")
        print(f"URL: {article['url']}")
        
        content_data = agent.extract_full_article_content(article['url'])
        
        if content_data.get('extraction_success'):
            print(f"✅ Success! Extracted {content_data.get('word_count', 0)} words")
            print(f"Title: {content_data.get('title', 'N/A')}")
            print(f"Content preview: {content_data.get('content', '')[:200]}...")
        else:
            print(f"❌ Failed: {content_data.get('error', 'Unknown error')}")
    
    # Test enrichment process
    print(f"\n🔍 Testing Article Enrichment...")
    enriched = agent.enrich_articles_with_content(test_articles, max_articles=2)
    
    print(f"Enriched {len(enriched)} articles:")
    for article in enriched:
        print(f"- {article.get('title', 'Unknown')}: {article.get('word_count', 0)} words extracted")
    
    # Test news analysis with current date
    print(f"\n🧠 Testing News Analysis with Current Date...")
    print(f"Current date: {datetime.now().strftime('%B %d, %Y')}")
    
    analysis_result = agent.analyze_news_clusters(test_articles)
    
    if analysis_result.get('status') == 'success':
        print("✅ Analysis successful!")
        clusters = analysis_result.get('clusters', {})
        for cluster_id, cluster_data in clusters.items():
            print(f"\nCluster: {cluster_data['cluster_info']['display_name']}")
            print(f"Analysis: {cluster_data['analysis'][:200]}...")
            print(f"Content extracted: {cluster_data.get('content_extracted', False)}")
    else:
        print(f"❌ Analysis failed: {analysis_result.get('message', 'Unknown error')}")

if __name__ == "__main__":
    print("🚀 Advanced Content Extraction Test")
    print("=" * 50)
    print(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    print("=" * 50)
    
    try:
        test_content_extraction()
        print("\n✅ Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc() 