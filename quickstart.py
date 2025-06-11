#!/usr/bin/env python3
"""
AI News Monitor - Quick Start Guide
Interactive setup and testing script
"""

import os
import sys
import subprocess
import shutil

def print_banner():
    """Print welcome banner"""
    print("🤖 AI & Robotics Daily News Monitor")
    print("=" * 45)
    print("Welcome! Let's get you set up quickly.")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("Please run: pip install -r requirements.txt")
        return False

def setup_env_file():
    """Help user set up .env file"""
    print("\n🔧 Setting up environment configuration...")
    
    if os.path.exists('.env'):
        response = input("📄 .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Keeping existing .env file")
            return True
    
    if os.path.exists('env_example.txt'):
        shutil.copy('env_example.txt', '.env')
        print("✅ Created .env file from template")
        print("\n📝 Please edit the .env file with your API keys:")
        print("   1. GitHub Personal Access Token")
        print("   2. OpenAI API Key") 
        print("   3. NewsAPI Key")
        print("   4. Email configuration")
        print("\n🔗 API Key Links:")
        print("   • GitHub: https://github.com/settings/tokens")
        print("   • OpenAI: https://platform.openai.com/api-keys")
        print("   • NewsAPI: https://newsapi.org/register")
        print()
        
        input("Press Enter after you've configured your .env file...")
        return True
    else:
        print("❌ env_example.txt not found")
        return False

def run_setup_check():
    """Run the setup verification"""
    print("\n🔍 Running setup verification...")
    try:
        result = subprocess.run([sys.executable, "setup_check.py"], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ setup_check.py not found")
        return False

def run_test():
    """Run a test of the system"""
    print("\n🧪 Running test of the monitoring system...")
    response = input("This will test all APIs and generate a sample digest. Continue? (Y/n): ")
    
    if response.lower() in ['', 'y', 'yes']:
        try:
            subprocess.run([sys.executable, "main.py", "--run-once"])
            return True
        except KeyboardInterrupt:
            print("\n⏹️ Test interrupted by user")
            return False
    else:
        print("Test skipped")
        return True

def show_next_steps():
    """Show next steps to user"""
    print("\n🎉 Setup Complete!")
    print("\n📋 Next Steps:")
    print("   1. Test the system: python main.py --run-once")
    print("   2. Start daily monitoring: python main.py --schedule")
    print("   3. Check logs: tail -f ai_news_monitor.log")
    print("\n📖 For more info, check README.md")
    print("\n🚀 Happy monitoring!")

def main():
    """Main quickstart function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Setup .env file
    if not setup_env_file():
        return False
    
    # Run setup check
    if not run_setup_check():
        print("\n⚠️ Setup verification failed")
        print("Please fix the issues above before continuing")
        return False
    
    # Offer to run test
    if run_test():
        show_next_steps()
        return True
    else:
        print("\n⚠️ Test failed - check the logs for details")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 