import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
import logging
from config import GITHUB_TOKEN, GITHUB_REPOS, GITHUB_COMMITS_LIMIT
from utils import rate_limit, safe_request, get_yesterday_date

logger = logging.getLogger(__name__)

class GitHubMonitor:
    def __init__(self):
        self.headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'
    
    @rate_limit(calls_per_minute=30)
    def get_recent_commits(self, repo: str, since_date: str = None) -> List[Dict[str, Any]]:
        """Get recent commits for a repository"""
        if not since_date:
            since_date = get_yesterday_date()
        
        url = f"{self.base_url}/repos/{repo}/commits"
        params = {
            'since': f"{since_date}T00:00:00Z",
            'per_page': GITHUB_COMMITS_LIMIT
        }
        
        try:
            response = safe_request(url, headers=self.headers, params=params)
            commits = response.json()
            
            processed_commits = []
            for commit in commits:
                commit_data = {
                    'repo': repo,
                    'sha': commit['sha'][:8],
                    'message': commit['commit']['message'].split('\n')[0],  # First line only
                    'author': commit['commit']['author']['name'],
                    'date': commit['commit']['author']['date'],
                    'url': commit['html_url']
                }
                processed_commits.append(commit_data)
            
            logger.info(f"Found {len(processed_commits)} commits for {repo}")
            return processed_commits
            
        except Exception as e:
            logger.error(f"Error fetching commits for {repo}: {e}")
            return []
    
    @rate_limit(calls_per_minute=30)
    def get_top_contributors(self, repo: str) -> List[Dict[str, Any]]:
        """Get top contributors for a repository"""
        url = f"{self.base_url}/repos/{repo}/contributors"
        params = {'per_page': 5}  # Top 5 contributors
        
        try:
            response = safe_request(url, headers=self.headers, params=params)
            contributors = response.json()
            
            processed_contributors = []
            for contributor in contributors:
                contributor_data = {
                    'repo': repo,
                    'username': contributor['login'],
                    'contributions': contributor['contributions'],
                    'profile_url': contributor['html_url'],
                    'avatar_url': contributor['avatar_url']
                }
                processed_contributors.append(contributor_data)
            
            logger.info(f"Found {len(processed_contributors)} top contributors for {repo}")
            return processed_contributors
            
        except Exception as e:
            logger.error(f"Error fetching contributors for {repo}: {e}")
            return []
    
    def monitor_all_repos(self) -> Dict[str, Any]:
        """Monitor all configured repositories"""
        github_data = {
            'commits': [],
            'contributors': {}
        }
        
        logger.info("Starting GitHub monitoring...")
        
        for repo in GITHUB_REPOS:
            logger.info(f"Monitoring repository: {repo}")
            
            # Get recent commits
            commits = self.get_recent_commits(repo)
            github_data['commits'].extend(commits)
            
            # Get top contributors
            contributors = self.get_top_contributors(repo)
            github_data['contributors'][repo] = contributors
        
        logger.info(f"GitHub monitoring complete. Found {len(github_data['commits'])} total commits")
        return github_data

if __name__ == "__main__":
    monitor = GitHubMonitor()
    data = monitor.monitor_all_repos()
    print(f"Commits: {len(data['commits'])}")
    print(f"Repositories monitored: {len(data['contributors'])}") 