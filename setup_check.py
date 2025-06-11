#!/usr/bin/env python3
"""
Setup Check Script for AI News Monitor
Verifies that all API keys and configuration are properly set
"""

import os
import sys
from dotenv import load_dotenv
import requests

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("📝 Please copy env_example.txt to .env and configure your API keys")
        return False
    
    load_dotenv()
    print("✅ .env file found")
    return True

def check_api_keys():
    """Check if all required API keys are present"""
    required_keys = {
        'GITHUB_TOKEN': 'GitHub Personal Access Token',
        'OPENAI_API_KEY': 'OpenAI API Key',
        'NEWS_API_KEY': 'NewsAPI Key',
        'EMAIL_SENDER': 'Email Sender Address',
        'EMAIL_PASSWORD': 'Email App Password',
        'EMAIL_RECIPIENT': 'Email Recipient Address'
    }
    
    missing_keys = []
    
    for key, description in required_keys.items():
        value = os.getenv(key)
        if not value or value.startswith('your_'):
            missing_keys.append(f"{key} ({description})")
            print(f"❌ {key} is missing or not configured")
        else:
            print(f"✅ {key} is configured")
    
    if missing_keys:
        print(f"\n📝 Please configure the following in your .env file:")
        for key in missing_keys:
            print(f"   - {key}")
        return False
    
    return True

def test_github_api():
    """Test GitHub API connection"""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        return False
    
    try:
        headers = {'Authorization': f'token {token}'}
        response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ GitHub API: Connected as {user_data.get('login', 'Unknown')}")
            return True
        else:
            print(f"❌ GitHub API: Error {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ GitHub API: Connection failed - {e}")
        return False

def test_openai_api():
    """Test OpenAI API connection"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return False
    
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        
        print("✅ OpenAI API: Connected successfully")
        return True
    except Exception as e:
        print(f"❌ OpenAI API: Connection failed - {e}")
        return False

def test_news_api():
    """Test NewsAPI connection"""
    api_key = os.getenv('NEWS_API_KEY')
    if not api_key:
        return False
    
    try:
        params = {
            'q': 'test',
            'pageSize': 1,
            'apiKey': api_key
        }
        response = requests.get('https://newsapi.org/v2/everything', params=params, timeout=10)
        
        if response.status_code == 200:
            print("✅ NewsAPI: Connected successfully")
            return True
        else:
            data = response.json()
            print(f"❌ NewsAPI: Error - {data.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ NewsAPI: Connection failed - {e}")
        return False

def test_email_config():
    """Test email configuration"""
    required_email_fields = ['EMAIL_SENDER', 'EMAIL_PASSWORD', 'EMAIL_RECIPIENT']
    
    for field in required_email_fields:
        value = os.getenv(field)
        if not value or value.startswith('your_'):
            print(f"❌ Email: {field} not configured")
            return False
    
    print("✅ Email: Configuration appears complete")
    print("📧 Note: Actual email sending will be tested when you run the system")
    return True

def main():
    """Main setup check function"""
    print("🔧 AI News Monitor - Setup Check")
    print("=" * 40)
    
    checks_passed = 0
    total_checks = 6
    
    # Check .env file
    if check_env_file():
        checks_passed += 1
    
    print()
    
    # Check API keys presence
    if check_api_keys():
        checks_passed += 1
    
    print()
    
    # Test API connections
    if test_github_api():
        checks_passed += 1
    
    if test_openai_api():
        checks_passed += 1
    
    if test_news_api():
        checks_passed += 1
    
    if test_email_config():
        checks_passed += 1
    
    print()
    print("=" * 40)
    print(f"Setup Check Results: {checks_passed}/{total_checks} passed")
    
    if checks_passed == total_checks:
        print("🎉 All checks passed! You're ready to run the AI News Monitor")
        print("🚀 Try running: python main.py --run-once")
    else:
        print("⚠️  Some checks failed. Please fix the issues above before running")
        print("📖 Check the README.md for detailed setup instructions")
    
    return checks_passed == total_checks

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 