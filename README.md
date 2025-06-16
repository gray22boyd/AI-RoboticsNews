%%% This Project is 97% Vibe Coded%%%%

# 🤖 AI & Robotics Intelligence Digest

An intelligent news monitoring system that automatically generates professional daily digests of AI and robotics developments by clustering and analyzing GitHub commits, research papers, and industry news using GPT-4.

## ✨ Features

- **🧠 Intelligent Clustering**: Automatically groups content by topics (OpenAI, DeepMind, Humanoids, etc.)
- **📊 Multi-Source Analysis**: Monitors GitHub repos, Papers with Code, and RSS news feeds
- **🎯 GPT-4 Powered**: Dynamic executive summaries and strategic insights
- **📧 Professional Email Digest**: Clean, scannable HTML email format
- **🔍 Relevance Filtering**: High-quality content filtering (6.5+ relevance threshold)
- **🚫 No Paywalls**: Uses free RSS feeds instead of paywalled news sources

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   Intelligence  │    │     Output      │
│                 │    │    Engine       │    │                 │
│ • GitHub API    │───▶│ • Topic         │───▶│ • HTML Email    │
│ • Papers w/Code │    │   Clustering    │    │ • Executive     │
│ • RSS Feeds     │    │ • GPT-4 Analysis│    │   Summary       │
│ • News APIs     │    │ • Cross-linking │    │ • Strategic     │
└─────────────────┘    └─────────────────┘    │   Insights      │
                                              └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- GitHub token
- NewsAPI key (optional)
- Email account for sending

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-robotics-digest.git
   cd ai-robotics-digest
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the system**
   ```bash
   python main.py --test  # Test run
   python main.py         # Full run with email
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with:

```env
# Required
OPENAI_API_KEY=your_openai_api_key
GITHUB_TOKEN=your_github_token

# Email Configuration
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENT=recipient@email.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Optional
NEWS_API_KEY=your_newsapi_key
```

### Monitored Sources

**GitHub Repositories:**
- pytorch/pytorch
- huggingface/transformers
- optuna/optuna
- mlflow/mlflow

**Research Papers:**
- Papers with Code API
- Keywords: deepmind, openai, robotics, transformer, etc.

**News Sources:**
- Free RSS feeds (OpenAI Blog, Google AI, NVIDIA, etc.)
- No paywall issues

## 📊 Sample Output

### Executive Summary
> "Today's intelligence reveals significant activity in three key areas. OpenAI developments show continued focus on privacy and integration capabilities, while robotics research demonstrates advances in embodied AI systems."

### Topic Clusters
- **🧠 OpenAI: Privacy, Integrations, and Reasoning Advances**
- **🤖 Humanoids & Physical AI: Embodied Intelligence** 
- **🔬 DeepMind & Google AI: Research Breakthroughs**

## 🛠️ Advanced Usage

### Custom Topics

Add new topic clusters in `summarize_agent.py`:

```python
self.topic_clusters = {
    'your_topic': {
        'keywords': ['keyword1', 'keyword2'],
        'display_name': '🎯 Your Topic Name',
        'icon': '🎯'
    }
}
```

### RSS Feeds

Add new sources in `config.py`:

```python
FREE_RSS_FEEDS = [
    {
        'name': 'Your Source',
        'url': 'https://example.com/feed.xml',
        'category': 'Company'
    }
]
```

## 📁 Project Structure

```
ai-robotics-digest/
├── main.py                 # Main execution script
├── summarize_agent.py      # GPT-4 clustering & analysis
├── email_agent.py          # HTML email generation
├── github_monitor.py       # GitHub API monitoring
├── paperswithcode_monitor.py # Research paper monitoring
├── rss_news_monitor.py     # RSS feed monitoring
├── news_monitor.py         # NewsAPI monitoring (backup)
├── config.py              # Configuration settings
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

## 🔧 Development

### Running Tests

```bash
python main.py --test
```

### Adding New Data Sources

1. Create a new monitor class in `monitors/`
2. Implement the required interface
3. Add to `main.py` data collection
4. Update clustering keywords if needed

### Customizing Email Format

Edit `email_agent.py`:
- Modify CSS styles
- Change section layouts
- Add new content types

## 📈 Monitoring & Logs

The system provides detailed logging:

```
2025-06-11 16:21:59,649 - paperswithcode_monitor - INFO - Found 67 papers from top organizations
2025-06-11 16:21:59,650 - __main__ - INFO - GitHub commits: 33
2025-06-11 16:21:59,650 - __main__ - INFO - Papers: 15
2025-06-11 16:21:59,650 - __main__ - INFO - News articles: 10
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Papers with Code for research data
- GitHub for development insights
- RSS feed providers for news content

## 📞 Support

- Create an [Issue](https://github.com/yourusername/ai-robotics-digest/issues) for bugs
- Start a [Discussion](https://github.com/yourusername/ai-robotics-digest/discussions) for questions
- Check the [Wiki](https://github.com/yourusername/ai-robotics-digest/wiki) for detailed docs

---

**Made with ❤️ for the AI & Robotics community** 
