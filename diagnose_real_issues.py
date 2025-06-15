#!/usr/bin/env python3
"""
Diagnose Real Data Collection Issues
Find out why the system isn't collecting REAL data
"""

import os
import sys
from datetime import datetime

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 CHECKING ENVIRONMENT CONFIGURATION...")
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("❌ CRITICAL: .env file is missing!")
        print("   This is why your system can't access API keys")
        return False
    
    # Load environment
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ .env file loaded")
    except ImportError:
        print("❌ python-dotenv not installed")
        return False
    
    # Check critical API keys
    github_token = os.getenv('GITHUB_TOKEN')
    openai_key = os.getenv('OPENAI_API_KEY')
    news_key = os.getenv('NEWS_API_KEY')
    
    issues = []
    
    if not github_token:
        issues.append("GITHUB_TOKEN missing")
    elif not github_token.startswith('ghp_'):
        issues.append("GITHUB_TOKEN format invalid")
    else:
        print(f"✅ GitHub token: {github_token[:10]}...")
    
    if not openai_key:
        issues.append("OPENAI_API_KEY missing")
    elif not openai_key.startswith('sk-'):
        issues.append("OPENAI_API_KEY format invalid")
    else:
        print(f"✅ OpenAI key: {openai_key[:10]}...")
    
    if not news_key:
        issues.append("NEWS_API_KEY missing")
    else:
        print(f"✅ News API key: {news_key[:10]}...")
    
    if issues:
        print("❌ API KEY ISSUES:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    
    return True

def test_github_api():
    """Test GitHub API directly"""
    print("\n🔍 TESTING GITHUB API DIRECTLY...")
    
    try:
        import requests
        from datetime import datetime, timedelta
        
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            print("❌ No GitHub token available")
            return False
        
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Test with a known active repo
        test_repo = 'pytorch/pytorch'
        since_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        url = f"https://api.github.com/repos/{test_repo}/commits"
        params = {
            'since': f"{since_date}T00:00:00Z",
            'per_page': 5
        }
        
        print(f"   Testing repo: {test_repo}")
        print(f"   Since date: {since_date}")
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            commits = response.json()
            print(f"✅ GitHub API working: {len(commits)} commits found")
            if commits:
                print(f"   Sample commit: {commits[0]['commit']['message'][:50]}...")
            return True
        else:
            print(f"❌ GitHub API failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ GitHub API test failed: {e}")
        return False

def test_news_api():
    """Test News API directly"""
    print("\n🔍 TESTING NEWS API DIRECTLY...")
    
    try:
        import requests
        from datetime import datetime, timedelta
        
        news_key = os.getenv('NEWS_API_KEY')
        if not news_key:
            print("❌ No News API key available")
            return False
        
        # Test with a simple AI query
        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': 'artificial intelligence',
            'apiKey': news_key,
            'language': 'en',
            'sortBy': 'relevancy',
            'from': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
            'pageSize': 5
        }
        
        print(f"   Testing query: artificial intelligence")
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            print(f"✅ News API working: {len(articles)} articles found")
            if articles:
                print(f"   Sample article: {articles[0]['title'][:50]}...")
            return True
        else:
            print(f"❌ News API failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ News API test failed: {e}")
        return False

def test_papers_api():
    """Test Papers With Code API directly"""
    print("\n🔍 TESTING PAPERS WITH CODE API DIRECTLY...")
    
    try:
        import requests
        
        # Test with a simple query
        url = 'https://paperswithcode.com/api/v1/papers'
        params = {
            'q': 'transformer',
            'ordering': '-published'
        }
        
        print(f"   Testing query: transformer")
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            papers = data.get('results', [])
            print(f"✅ Papers API working: {len(papers)} papers found")
            if papers:
                print(f"   Sample paper: {papers[0]['title'][:50]}...")
            return True
        else:
            print(f"❌ Papers API failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Papers API test failed: {e}")
        return False

def test_monitor_classes():
    """Test the actual monitor classes"""
    print("\n🔍 TESTING MONITOR CLASSES...")
    
    try:
        from github_monitor import GitHubMonitor
        from news_monitor import NewsMonitor
        from paperswithcode_monitor import PapersWithCodeMonitor
        
        print("✅ All monitor classes imported")
        
        # Test GitHub Monitor
        try:
            github_monitor = GitHubMonitor()
            github_data = github_monitor.monitor_all_repos()
            commits = github_data.get('commits', [])
            print(f"✅ GitHub Monitor: {len(commits)} commits collected")
        except Exception as e:
            print(f"❌ GitHub Monitor failed: {e}")
        
        # Test News Monitor
        try:
            news_monitor = NewsMonitor()
            news_data = news_monitor.monitor_all_keywords()
            print(f"✅ News Monitor: {len(news_data)} articles collected")
        except Exception as e:
            print(f"❌ News Monitor failed: {e}")
        
        # Test Papers Monitor
        try:
            papers_monitor = PapersWithCodeMonitor()
            papers_data = papers_monitor.monitor_all_keywords()
            print(f"✅ Papers Monitor: {len(papers_data)} papers collected")
        except Exception as e:
            print(f"❌ Papers Monitor failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Monitor class test failed: {e}")
        return False

def main():
    """Run all real issue diagnostics"""
    print("🚨 DIAGNOSING REAL DATA COLLECTION ISSUES")
    print("=" * 60)
    print("NO FAKE DATA - FINDING ACTUAL PROBLEMS")
    print("=" * 60)
    
    tests = [
        ("Environment Configuration", check_environment),
        ("GitHub API Direct Test", test_github_api),
        ("News API Direct Test", test_news_api),
        ("Papers API Direct Test", test_papers_api),
        ("Monitor Classes Test", test_monitor_classes)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 REAL ISSUE DIAGNOSIS SUMMARY")
    print(f"{'='*60}")
    
    for test_name, result in results.items():
        status = "✅ WORKING" if result else "❌ BROKEN"
        print(f"{status} {test_name}")
    
    failed_tests = [name for name, result in results.items() if not result]
    
    if failed_tests:
        print(f"\n🚨 REAL ISSUES FOUND:")
        for test in failed_tests:
            print(f"   - {test}")
        print(f"\n🔧 FIX THESE ISSUES TO GET REAL DATA")
    else:
        print(f"\n🎉 ALL SYSTEMS WORKING - Data collection should work!")

if __name__ == "__main__":
    main() 