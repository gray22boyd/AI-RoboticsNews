#!/usr/bin/env python3
"""
Safe Daily AI & Robotics Intelligence Digest Scheduler
Uses existing working components to avoid ArXiv issues
"""

import os
import sys
import time
import logging
import smtplib
import schedule
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('daily_digest.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import existing working components
from github_monitor import GitHubMonitor
from news_monitor import NewsMonitor
from paperswithcode_monitor import PapersWithCodeMonitor
from intelligent_summarize_agent import IntelligentSummarizeAgent
from enhanced_email_agent import EnhancedEmailAgent

class SafeDailyDigestScheduler:
    def __init__(self):
        """Initialize the safe daily digest scheduler"""
        logger.info("🔧 Initializing SAFE Daily Digest Scheduler with existing working components...")
        self.load_config()
        self.setup_monitors()
        
    def load_config(self):
        """Load configuration from environment variables"""
        # Load environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv()
            logger.info("✅ Environment variables loaded from .env file")
        except ImportError:
            logger.warning("python-dotenv not installed, using system environment variables")
        
        # Email configuration (using existing variable names)
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('EMAIL_SENDER')
        self.sender_password = os.getenv('EMAIL_PASSWORD')
        self.recipient_email = os.getenv('EMAIL_RECIPIENT')
        
        # API Keys (using existing variable names)
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')
        
        # Validate required configuration
        required_vars = [
            'EMAIL_SENDER', 'EMAIL_PASSWORD', 'EMAIL_RECIPIENT',
            'GITHUB_TOKEN', 'OPENAI_API_KEY'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        logger.info("✅ Configuration loaded successfully")
        
    def setup_monitors(self):
        """Initialize monitoring agents using existing working components"""
        try:
            self.github_monitor = GitHubMonitor()
            self.news_monitor = NewsMonitor()
            self.papers_monitor = PapersWithCodeMonitor()
            self.summarize_agent = IntelligentSummarizeAgent()
            self.email_agent = EnhancedEmailAgent()
            logger.info("✅ All monitoring agents initialized with existing working components")
        except Exception as e:
            logger.error(f"❌ Error initializing monitors: {e}")
            raise
    
    def collect_fresh_data(self) -> Dict[str, Any]:
        """Collect fresh data using existing working systems"""
        logger.info("🔍 Collecting fresh data using proven working systems...")
        
        collected_data = {
            'github': {'commits': []},
            'news': [],
            'papers': [],
            'collection_time': datetime.now().isoformat(),
            'source': 'existing_working_systems',
            'errors': []
        }
        
        # GitHub data collection with detailed error handling
        try:
            logger.info("📊 Fetching GitHub activity...")
            github_data = self.github_monitor.monitor_all_repos()
            collected_data['github'] = github_data
            logger.info(f"   ✅ GitHub commits collected: {len(github_data.get('commits', []))}")
            
            if github_data.get('commits'):
                sample_commit = github_data['commits'][0]
                logger.info(f"   📝 Sample commit: {sample_commit.get('message', 'No message')[:50]}...")
            else:
                logger.warning("   ⚠️ No GitHub commits found")
                
        except Exception as e:
            error_msg = f"GitHub collection failed: {str(e)}"
            logger.error(f"❌ {error_msg}")
            collected_data['errors'].append(error_msg)
        
        # News data collection with detailed error handling
        try:
            logger.info("📰 Fetching news articles...")
            news_data = self.news_monitor.monitor_all_keywords()
            collected_data['news'] = news_data
            logger.info(f"   ✅ News articles collected: {len(news_data)}")
            
            if news_data:
                sample_article = news_data[0]
                logger.info(f"   📰 Sample article: {sample_article.get('title', 'No title')[:50]}...")
            else:
                logger.warning("   ⚠️ No news articles found")
                
        except Exception as e:
            error_msg = f"News collection failed: {str(e)}"
            logger.error(f"❌ {error_msg}")
            collected_data['errors'].append(error_msg)
        
        # Papers data collection with detailed error handling
        try:
            logger.info("📚 Fetching research papers...")
            papers_data = self.papers_monitor.monitor_all_keywords()
            collected_data['papers'] = papers_data
            logger.info(f"   ✅ Research papers collected: {len(papers_data)}")
            
            if papers_data:
                sample_paper = papers_data[0]
                logger.info(f"   📚 Sample paper: {sample_paper.get('title', 'No title')[:50]}...")
            else:
                logger.warning("   ⚠️ No research papers found")
                
        except Exception as e:
            error_msg = f"Papers collection failed: {str(e)}"
            logger.error(f"❌ {error_msg}")
            collected_data['errors'].append(error_msg)
        
        # Summary of collection results
        github_count = len(collected_data['github'].get('commits', []))
        news_count = len(collected_data['news'])
        papers_count = len(collected_data['papers'])
        total_items = github_count + news_count + papers_count
        
        logger.info(f"✅ DETAILED DATA COLLECTION SUMMARY:")
        logger.info(f"   - GitHub commits: {github_count}")
        logger.info(f"   - News articles: {news_count}")
        logger.info(f"   - Research papers: {papers_count}")
        logger.info(f"   - TOTAL ITEMS: {total_items}")
        logger.info(f"   - Errors encountered: {len(collected_data['errors'])}")
        
        if collected_data['errors']:
            logger.warning("⚠️ Collection errors:")
            for error in collected_data['errors']:
                logger.warning(f"   - {error}")
        
        if total_items == 0:
            logger.error("❌ CRITICAL: NO DATA COLLECTED FROM ANY SOURCE - EMAIL WILL BE EMPTY!")
            logger.error("❌ This will result in an empty email. Using fallback data.")
            return self.get_fallback_data()
        else:
            logger.info(f"🎉 SUCCESS: {total_items} total items collected - email will have content!")
        
        return collected_data
    
    def get_fallback_data(self) -> Dict[str, Any]:
        """Return empty data structure when collection fails - NO FAKE DATA"""
        logger.error("❌ CRITICAL: Data collection completely failed - returning empty structure")
        logger.error("❌ NO FAKE DATA WILL BE CREATED - Fix the data collection issues!")
        
        return {
            'github': {'commits': []},
            'news': [],
            'papers': [],
            'collection_time': datetime.now().isoformat(),
            'fallback': True,
            'errors': ['All data collection methods failed']
        }
    
    def generate_daily_digest(self) -> str:
        """Generate the daily intelligence digest using existing working systems"""
        logger.info("🧠 Generating daily intelligence digest with proven components...")
        
        try:
            daily_data = self.collect_fresh_data()
            
            digest_data = self.summarize_agent.create_intelligent_digest(
                github_data=daily_data['github'],
                papers_data=daily_data['papers'],
                news_data=daily_data['news']
            )
            
            email_content = self.email_agent.create_enhanced_email_content(
                digest_data=digest_data,
                github_data=daily_data['github'],
                papers_data=daily_data['papers'],
                news_data=daily_data['news']
            )
            
            logger.info("✅ Daily digest generated successfully using existing systems")
            return email_content
            
        except Exception as e:
            logger.error(f"❌ Error generating digest: {e}")
            return self.create_error_digest(str(e))
    
    def create_error_digest(self, error_message: str) -> str:
        """Create a simple error digest if generation fails"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AI Digest - Service Notice</title>
        </head>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>🔧 AI & Robotics Intelligence Digest - Service Notice</h2>
            <p><strong>Date:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p>We encountered an issue generating today's intelligence digest:</p>
            <div style="background: #f8f9fa; padding: 15px; border-left: 4px solid #dc3545; margin: 15px 0;">
                <code>{error_message}</code>
            </div>
            <p>Our team has been notified and will resolve this issue. You'll receive your next digest tomorrow.</p>
            <p><em>AI & Robotics Intelligence Team</em></p>
        </body>
        </html>
        """
    
    def send_email(self, html_content: str, subject: str = None) -> bool:
        """Send the digest via email"""
        if not subject:
            subject = f"AI & Robotics Intelligence Digest - {datetime.now().strftime('%B %d, %Y')}"
        
        logger.info(f"📧 Sending email to {self.recipient_email}...")
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = subject
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info("✅ Email sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error sending email: {e}")
            return False
    
    def run_daily_digest(self):
        """Main function to run the daily digest process"""
        logger.info("🚀 Starting SAFE daily AI & Robotics Intelligence Digest generation...")
        
        try:
            digest_content = self.generate_daily_digest()
            success = self.send_email(digest_content)
            
            if success:
                logger.info("🎉 Daily digest completed successfully using existing systems!")
            else:
                logger.error("❌ Daily digest completed with email errors")
                
        except Exception as e:
            logger.error(f"❌ Critical error in daily digest: {e}")
            error_content = self.create_error_digest(str(e))
            self.send_email(error_content, "AI Digest - Service Error")
    
    def start_scheduler(self):
        """Start the daily scheduler"""
        logger.info("⏰ Starting SAFE daily digest scheduler...")
        logger.info("📅 Scheduled to run daily at 7:30 AM using existing working systems")
        
        schedule.every().day.at("07:30").do(self.run_daily_digest)
        
        logger.info("✅ Safe scheduler started. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            logger.info("🛑 Scheduler stopped by user")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Safe AI & Robotics Daily Digest Scheduler')
    parser.add_argument('--test', action='store_true', help='Run digest immediately for testing')
    parser.add_argument('--schedule', action='store_true', help='Start the daily scheduler')
    
    args = parser.parse_args()
    
    try:
        scheduler = SafeDailyDigestScheduler()
        
        if args.test:
            logger.info("🧪 Running test digest using existing working systems...")
            scheduler.run_daily_digest()
        elif args.schedule:
            scheduler.start_scheduler()
        else:
            print("Safe Daily Digest Scheduler - Uses existing working components")
            print("Usage:")
            print("  python daily_scheduler_safe.py --test      # Run digest now")
            print("  python daily_scheduler_safe.py --schedule  # Start daily scheduler")
            
    except Exception as e:
        logger.error(f"❌ Failed to start safe scheduler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 