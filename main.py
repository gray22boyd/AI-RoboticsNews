#!/usr/bin/env python3
"""
AI News Agent - Main orchestration script
Monitors GitHub, research papers, and news for AI & robotics developments
"""

import logging
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json

from github_monitor import GitHubMonitor
from paperswithcode_monitor import PapersWithCodeMonitor
from news_monitor import NewsMonitor
from summarize_agent import SummarizeAgent
from email_sender import EmailSender
from config import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_config():
    """Validate all required configuration is present"""
    required_keys = {
        'GITHUB_TOKEN': GITHUB_TOKEN,
        'OPENAI_API_KEY': OPENAI_API_KEY,
        'NEWS_API_KEY': NEWS_API_KEY,
        'EMAIL_SENDER': EMAIL_SENDER,
        'EMAIL_PASSWORD': EMAIL_PASSWORD,
        'EMAIL_RECIPIENT': EMAIL_RECIPIENT
    }
    
    config_status = {}
    for key, value in required_keys.items():
        is_present = bool(value and value.strip())
        is_placeholder = value in ['your_api_key_here', 'your_email_here', 'your_password_here'] if value else True
        config_status[key] = {
            'present': is_present,
            'is_placeholder': is_placeholder,
            'length': len(value) if value else 0
        }
    
    logger.info(f"🔍 Config Status: {config_status}")
    
    # Check for missing or placeholder values
    missing_keys = [k for k, v in config_status.items() if not v['present'] or v['is_placeholder']]
    
    if missing_keys:
        logger.error(f"❌ Missing or placeholder configuration for: {missing_keys}")
        logger.error("Please check your .env file and ensure all API keys are properly set")
        return False
    
    logger.info("✅ All API keys are properly configured!")
    return True

def collect_github_data():
    """Collect GitHub data"""
    try:
        github_monitor = GitHubMonitor()
        return github_monitor.monitor_all_repos()
    except Exception as e:
        logger.error(f"GitHub monitoring failed: {e}")
        return {'commits': [], 'contributors': {}}

def collect_papers_data():
    """Collect Papers With Code data"""
    try:
        papers_monitor = PapersWithCodeMonitor()
        return papers_monitor.monitor_all_keywords()
    except Exception as e:
        logger.error(f"Papers With Code monitoring failed: {e}")
        return []

def collect_news_data():
    """Collect news data from free RSS sources (no paywalls)"""
    try:
        from rss_news_monitor import RSSNewsMonitor
        news_monitor = RSSNewsMonitor()
        return news_monitor.monitor_all_feeds()
    except Exception as e:
        logger.error(f"RSS news monitoring failed: {e}")
        # Fallback to original NewsAPI if RSS fails
        try:
            news_monitor = NewsMonitor()
            return news_monitor.monitor_all_keywords()
        except Exception as e2:
            logger.error(f"Fallback news monitoring also failed: {e2}")
            return []

def main():
    parser = argparse.ArgumentParser(description='AI News Agent - Monitor and digest AI/Robotics developments')
    parser.add_argument('--schedule', choices=['daily', 'weekly'], help='Schedule for automated runs')
    parser.add_argument('--test', action='store_true', help='Run in test mode (single execution)')
    args = parser.parse_args()

    if not args.schedule and not args.test:
        logger.info("No arguments provided. Running once for testing...")
        args.test = True

    logger.info("=" * 50)
    logger.info("Starting daily AI & Robotics digest generation")
    logger.info("=" * 50)

    # Validate configuration
    logger.info("🔍 Config Check - Checking API key configuration...")
    if not validate_config():
        logger.error("❌ Configuration validation failed. Exiting...")
        return

    # Start data collection in parallel
    logger.info("Starting parallel data collection...")
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all monitoring tasks
        github_future = executor.submit(collect_github_data)
        papers_future = executor.submit(collect_papers_data)
        news_future = executor.submit(collect_news_data)
        
        # Collect results as they complete
        github_data = None
        papers_data = None
        news_data = None
        
        for future in as_completed([github_future, papers_future, news_future]):
            try:
                if future == github_future:
                    github_data = future.result()
                    logger.info("GitHub monitoring completed")
                elif future == papers_future:
                    papers_data = future.result()
                    logger.info("Papers With Code monitoring completed")
                elif future == news_future:
                    news_data = future.result()
                    logger.info("News monitoring completed")
            except Exception as e:
                logger.error(f"A monitoring task failed: {e}")

    # Provide fallback data if any monitoring failed
    if github_data is None:
        github_data = {'commits': [], 'contributors': {}}
    if papers_data is None:
        papers_data = []
    if news_data is None:
        news_data = []

    # Log collection summary
    logger.info("=" * 50)
    logger.info("DATA COLLECTION SUMMARY")
    logger.info("=" * 50)
    logger.info(f"  GitHub commits: {len(github_data.get('commits', []))}")
    logger.info(f"  Papers: {len(papers_data)}")
    logger.info(f"  News articles: {len(news_data)}")
    
    # Validate we have meaningful data to summarize
    has_github_data = bool(github_data.get('commits'))
    has_papers_data = bool(papers_data)
    has_news_data = bool(news_data)
    
    if not any([has_github_data, has_papers_data, has_news_data]):
        logger.error("❌ No data collected from any sources - cannot generate digest")
        return
    
    # Log what data we have for summarization
    data_sources = []
    if has_github_data:
        data_sources.append("GitHub")
    if has_papers_data:
        data_sources.append("Papers")
    if has_news_data:
        data_sources.append("News")
    
    logger.info(f"📊 Proceeding with summarization using: {', '.join(data_sources)}")

    # Generate intelligent digest with clustering
    logger.info("🧠 Generating intelligent AI digest with clustering and analysis...")
    try:
        from summarize_agent import IntelligentSummarizeAgent
        from email_agent import IntelligentEmailAgent
        
        # Create intelligent analysis
        summarizer = IntelligentSummarizeAgent()
        digest_data = summarizer.create_intelligent_digest(github_data, papers_data, news_data)
        
        # Generate email content
        email_agent = IntelligentEmailAgent()
        email_content = email_agent.create_intelligent_email_content(digest_data, github_data, papers_data, news_data)
        
        # Send email
        logger.info("📧 Sending email digest...")
        email_sender = EmailSender()
        success = email_sender.send_digest(email_content)
        
        if success:
            logger.info("✅ AI Intelligence Digest sent successfully!")
            logger.info(f"📬 Delivered to: {EMAIL_RECIPIENT}")
        else:
            logger.error("❌ Failed to send email digest")
            
    except Exception as e:
        logger.error(f"💥 Failed to generate or send digest: {e}")
        logger.error("This may be due to API rate limits or configuration issues")

    logger.info("=" * 50)
    logger.info("Daily digest generation complete")
    logger.info("=" * 50)

if __name__ == "__main__":
    main() 