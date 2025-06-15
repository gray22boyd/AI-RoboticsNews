#!/usr/bin/env python3
"""
Enhanced Configuration for AI & Robotics Intelligence Digest
Includes settings for visual enhancements and actionable intelligence features
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Core API Keys (Required)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')

# Email Configuration (Required)
EMAIL_SENDER = os.getenv('EMAIL_SENDER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT', '')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))

# Email Subject and Branding
EMAIL_SUBJECT = os.getenv('EMAIL_SUBJECT', 'AI & Robotics Intelligence Digest')
DIGEST_BRANDING = {
    'title': 'AI & Robotics Intelligence Digest',
    'subtitle': 'Powered by GPT-4 Analysis',
    'description': 'Intelligent clustering and analysis of GitHub, research papers, and industry news'
}

# Enhanced Email Features
ENHANCED_EMAIL_FEATURES = {
    'visual_hierarchy': True,
    'activity_indicators': True,
    'trend_arrows': True,
    'urgency_classification': True,
    'action_items': True,
    'key_insights_cards': True,
    'executive_summary': True,
    'mobile_responsive': True,
    'dark_mode_support': False,  # Future feature
    'interactive_elements': False  # Future feature
}

# Activity Level Thresholds
ACTIVITY_THRESHOLDS = {
    'high': {
        'github_commits': 8,
        'research_papers': 4,
        'news_articles': 6
    },
    'medium': {
        'github_commits': 4,
        'research_papers': 2,
        'news_articles': 3
    },
    'low': {
        'github_commits': 1,
        'research_papers': 1,
        'news_articles': 1
    }
}

# Urgency Keywords for Classification
URGENCY_KEYWORDS = {
    'breaking': [
        'breaking', 'urgent', 'critical', 'emergency', 'immediate',
        'alert', 'crisis', 'major incident', 'security breach'
    ],
    'high': [
        'major', 'significant', 'important', 'breakthrough', 'milestone',
        'announcement', 'launch', 'release', 'acquisition', 'partnership'
    ],
    'medium': [
        'notable', 'interesting', 'development', 'update', 'progress',
        'improvement', 'enhancement', 'feature', 'research'
    ],
    'low': [
        'minor', 'small', 'routine', 'maintenance', 'patch',
        'fix', 'documentation', 'cleanup', 'refactor'
    ]
}

# Trend Analysis Keywords
TREND_KEYWORDS = {
    'increasing': [
        'growing', 'increasing', 'expanding', 'rising', 'surge', 'boom',
        'accelerating', 'scaling', 'adoption', 'momentum', 'uptick'
    ],
    'decreasing': [
        'declining', 'decreasing', 'falling', 'dropping', 'slowing',
        'reducing', 'downturn', 'contraction', 'retreat', 'pullback'
    ],
    'stable': [
        'steady', 'consistent', 'maintained', 'stable', 'unchanged',
        'plateau', 'flat', 'constant', 'regular', 'ongoing'
    ]
}

# Content Classification Tags
CONTENT_TAGS = {
    'breakthrough': [
        'breakthrough', 'first time', 'revolutionary', 'milestone', 'record',
        'unprecedented', 'groundbreaking', 'innovative', 'novel'
    ],
    'privacy': [
        'privacy', 'data protection', 'gdpr', 'surveillance', 'personal data',
        'encryption', 'security', 'confidential', 'anonymization'
    ],
    'deployment': [
        'deployment', 'production', 'commercial', 'enterprise', 'scaling',
        'rollout', 'implementation', 'adoption', 'integration'
    ],
    'research': [
        'research', 'study', 'paper', 'findings', 'experiment',
        'analysis', 'investigation', 'academic', 'scientific'
    ],
    'funding': [
        'funding', 'investment', 'series', 'valuation', 'acquisition',
        'ipo', 'venture', 'capital', 'financing', 'round'
    ],
    'open_source': [
        'open source', 'github', 'repository', 'community', 'free',
        'public', 'collaborative', 'contribution', 'fork'
    ]
}

# Visual Design Settings
VISUAL_DESIGN = {
    'primary_colors': {
        'blue': '#4299e1',
        'green': '#48bb78',
        'orange': '#ed8936',
        'purple': '#9f7aea',
        'red': '#f56565'
    },
    'gradients': {
        'header': 'linear-gradient(135deg, #1a365d 0%, #2d3748 100%)',
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'action_items': 'linear-gradient(135deg, #1a365d 0%, #2c5282 100%)',
        'strategic': 'linear-gradient(135deg, #553c9a 0%, #b83280 100%)'
    },
    'typography': {
        'font_family': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Helvetica Neue", Arial, sans-serif',
        'header_size': '32px',
        'section_size': '24px',
        'body_size': '15px'
    },
    'spacing': {
        'section_padding': '40px 30px',
        'card_padding': '20px',
        'grid_gap': '20px'
    }
}

# GPT-4 Analysis Settings
GPT_ANALYSIS = {
    'model': 'gpt-4',
    'temperature': 0.3,
    'max_tokens': {
        'executive_summary': 200,
        'action_items': 300,
        'strategic_insights': 250,
        'cluster_analysis': 200
    },
    'prompts': {
        'executive_summary_style': 'professional, analytical tone focusing on implications and actionable insights',
        'action_items_types': ['Monitor', 'Investigate', 'Evaluate', 'Prepare'],
        'strategic_focus': 'cross-cluster patterns and industry implications'
    }
}

# Monitoring Limits
MONITORING_LIMITS = {
    'github_commits': int(os.getenv('GITHUB_COMMITS_LIMIT', '33')),
    'research_papers': int(os.getenv('PAPERS_LIMIT', '15')),
    'news_articles': int(os.getenv('NEWS_ARTICLES_LIMIT', '10')),
    'max_clusters_display': 8,
    'max_insights_cards': 6,
    'max_action_items': 4
}

# Source Display Settings
SOURCE_DISPLAY = {
    'github': {
        'max_commits_shown': 6,
        'title_max_length': 60,
        'show_author': True,
        'show_sha': True
    },
    'papers': {
        'max_papers_shown': 5,
        'title_max_length': 80,
        'show_relevance_score': True,
        'min_relevance_threshold': 6.5
    },
    'news': {
        'max_articles_shown': 6,
        'title_max_length': 80,
        'show_source': True,
        'show_relevance_score': False
    }
}

# GitHub Repositories to Monitor
GITHUB_REPOS = [
    'openai/openai-python',
    'openai/openai-cookbook',
    'anthropic/anthropic-sdk-python',
    'google-deepmind/deepmind-research',
    'facebookresearch/llama',
    'microsoft/DeepSpeed',
    'huggingface/transformers',
    'pytorch/pytorch',
    'tensorflow/tensorflow',
    'NVIDIA/NeMo',
    'boston-dynamics/spot-sdk',
    'agility-robotics/agility-sdk',
    'tesla/autopilot',
    'waymo/waymo-open-dataset'
]

# Research Keywords for Papers with Code
RESEARCH_KEYWORDS = [
    'large language model', 'transformer', 'attention mechanism',
    'multimodal', 'vision transformer', 'diffusion model',
    'reinforcement learning', 'robotics', 'autonomous driving',
    'computer vision', 'natural language processing',
    'machine learning', 'deep learning', 'neural network',
    'artificial intelligence', 'AI safety', 'alignment'
]

# News Keywords (Organized by Category)
NEWS_KEYWORDS = {
    'companies': [
        'OpenAI', 'ChatGPT', 'GPT-4', 'Anthropic', 'Claude',
        'Google AI', 'DeepMind', 'Bard', 'Gemini',
        'Microsoft AI', 'Copilot', 'Azure AI',
        'Meta AI', 'LLaMA', 'Facebook AI',
        'Tesla', 'Autopilot', 'FSD',
        'NVIDIA', 'ChatGPT', 'AI chips'
    ],
    'technologies': [
        'artificial intelligence', 'machine learning', 'deep learning',
        'neural networks', 'transformer', 'large language model',
        'computer vision', 'natural language processing',
        'robotics', 'autonomous vehicles', 'self-driving'
    ],
    'applications': [
        'AI assistant', 'chatbot', 'code generation',
        'image generation', 'text generation',
        'autonomous driving', 'medical AI', 'AI drug discovery'
    ],
    'regulation': [
        'AI regulation', 'AI ethics', 'AI safety',
        'AI governance', 'AI policy', 'AI standards'
    ]
}

# RSS News Sources (Free, No Paywalls)
RSS_NEWS_SOURCES = [
    {
        'name': 'MIT Technology Review AI',
        'url': 'https://www.technologyreview.com/topic/artificial-intelligence/feed/',
        'category': 'research'
    },
    {
        'name': 'AI News',
        'url': 'https://artificialintelligence-news.com/feed/',
        'category': 'industry'
    },
    {
        'name': 'VentureBeat AI',
        'url': 'https://venturebeat.com/ai/feed/',
        'category': 'business'
    },
    {
        'name': 'The Verge AI',
        'url': 'https://www.theverge.com/ai-artificial-intelligence/rss/index.xml',
        'category': 'technology'
    },
    {
        'name': 'IEEE Spectrum AI',
        'url': 'https://spectrum.ieee.org/topic/artificial-intelligence/feed',
        'category': 'technical'
    }
]

# Export all settings
__all__ = [
    'OPENAI_API_KEY', 'GITHUB_TOKEN', 'NEWS_API_KEY',
    'EMAIL_SENDER', 'EMAIL_PASSWORD', 'EMAIL_RECIPIENT',
    'SMTP_SERVER', 'SMTP_PORT', 'EMAIL_SUBJECT',
    'ENHANCED_EMAIL_FEATURES', 'ACTIVITY_THRESHOLDS',
    'URGENCY_KEYWORDS', 'TREND_KEYWORDS', 'CONTENT_TAGS',
    'VISUAL_DESIGN', 'GPT_ANALYSIS', 'MONITORING_LIMITS',
    'SOURCE_DISPLAY', 'GITHUB_REPOS', 'RESEARCH_KEYWORDS',
    'NEWS_KEYWORDS', 'RSS_NEWS_SOURCES', 'DIGEST_BRANDING'
] 