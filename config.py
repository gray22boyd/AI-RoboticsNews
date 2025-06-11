"""
Configuration settings for AI & Robotics News Monitor
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

# Email Configuration
EMAIL_SENDER = os.getenv('EMAIL_SENDER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))

# Email Subject
EMAIL_SUBJECT = os.getenv('EMAIL_SUBJECT', 'Daily AI & Robotics Digest')

# GitHub Configuration
GITHUB_REPOS = [
    'pytorch/pytorch',
    'huggingface/transformers',
    'optuna/optuna',
    'mlflow/mlflow'
]

# Enhanced News Configuration with Diverse Keywords (as requested)
NEWS_KEYWORDS = [
    # Core AI Companies (Enhanced)
    'OpenAI',
    'DeepMind', 
    'Anthropic',
    'NVIDIA AI',
    'Tesla Robotics',
    'Google DeepMind',
    'Meta AI',
    'Microsoft AI',
    
    # Humanoid & Physical AI (Enhanced)
    'Figure AI',
    'Sanctuary AI', 
    'Boston Dynamics',
    '1X Technologies',
    'humanoid',
    'physical AI',
    'embodied AI',
    'robot learning',
    
    # AI Models & Technologies
    'ChatGPT',
    'Claude',
    'Gemini',
    'GPT-4',
    'Mistral',
    'foundation model',
    'large language model',
    'multimodal AI',
    
    # Robotics & Automation
    'autonomous vehicle',
    'self-driving',
    'robot manipulation',
    'industrial robotics',
    'service robotics',
    'AI regulation',
    'AI safety',
    
    # Emerging Companies & Terms
    'robotics startup',
    'AI breakthrough',
    'machine learning',
    'artificial intelligence',
    'neural network',
    'computer vision'
]

# Research papers configuration - Papers With Code
PAPERSWITHCODE_KEYWORDS = [
    'deepmind',
    'openai', 
    'anthropic',
    'gpt',
    'robotics',
    'transformer',
    'policy gradient',
    'foundation model',
    'humanoid',
    'embodied ai',
    '1x',
    'claude',
    'gemini',
    'figure ai',
    'boston dynamics',
    'sanctuary ai',
    'physical ai',
    'mistral',
    'retnet',
    'nvidia',
    'meta ai'
]
PAPERS_PER_TOPIC = 5

# Monitoring Limits
NEWS_ARTICLES_LIMIT = int(os.getenv('NEWS_ARTICLES_LIMIT', '10'))
GITHUB_COMMITS_LIMIT = int(os.getenv('GITHUB_COMMITS_LIMIT', '10'))

# Free RSS Feeds (No Paywall Issues)
FREE_RSS_FEEDS = [
    # Company Blogs (Always Free & High Quality)
    {
        'name': 'OpenAI Blog',
        'url': 'https://openai.com/blog/rss.xml',
        'category': 'Company'
    },
    {
        'name': 'Google AI Blog',
        'url': 'https://research.google/blog/rss/',
        'category': 'Company'
    },
    {
        'name': 'NVIDIA AI Blog',
        'url': 'https://blogs.nvidia.com/blog/category/deep-learning/feed/',
        'category': 'Company'
    },
    {
        'name': 'Hugging Face Blog',
        'url': 'https://huggingface.co/blog/feed.xml',
        'category': 'Company'
    },
    # Free Tech News Sites
    {
        'name': 'MIT Technology Review AI',
        'url': 'https://www.technologyreview.com/topic/artificial-intelligence/feed/',
        'category': 'News'
    },
    {
        'name': 'MarkTechPost',
        'url': 'https://marktechpost.com/feed',
        'category': 'News'
    },
    {
        'name': 'Unite.AI',
        'url': 'https://unite.ai/feed',
        'category': 'News'
    },
    {
        'name': 'DailyAI',
        'url': 'https://dailyai.com/feed',
        'category': 'News'
    },
    {
        'name': 'MIT News AI',
        'url': 'https://news.mit.edu/rss/topic/artificial-intelligence',
        'category': 'Academic'
    },
    {
        'name': 'TechCrunch AI',
        'url': 'https://techcrunch.com/category/artificial-intelligence/feed/',
        'category': 'News'
    },
    {
        'name': 'VentureBeat AI',
        'url': 'https://venturebeat.com/ai/feed/',
        'category': 'News'
    },
    {
        'name': 'AIhub',
        'url': 'https://aihub.org/feed/?cat=-473',
        'category': 'News'
    },
    # Academic/Research Sources
    {
        'name': 'BAIR Blog',
        'url': 'https://bair.berkeley.edu/blog/feed.xml',
        'category': 'Academic'
    },
    {
        'name': 'Machine Learning Mastery',
        'url': 'https://machinelearningmastery.com/blog/feed/',
        'category': 'Educational'
    }
]

# Rate Limiting (calls per minute)
GITHUB_RATE_LIMIT = 60
NEWS_RATE_LIMIT = 20
ARXIV_RATE_LIMIT = 10 