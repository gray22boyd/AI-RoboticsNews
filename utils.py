import time
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable
import requests
from retry import retry

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def rate_limit(calls_per_minute: int = 30):
    """Rate limiting decorator"""
    def decorator(func: Callable) -> Callable:
        last_called = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = 60.0 / calls_per_minute - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

@retry(tries=3, delay=1, backoff=2)
def safe_request(url: str, headers: dict = None, params: dict = None) -> requests.Response:
    """Make a safe HTTP request with retries"""
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for {url}: {e}")
        raise

def get_yesterday_date() -> str:
    """Get yesterday's date in YYYY-MM-DD format"""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

def get_last_week_date() -> str:
    """Get date from a week ago in YYYY-MM-DD format"""
    last_week = datetime.now() - timedelta(days=7)
    return last_week.strftime('%Y-%m-%d')

def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def format_date_readable(date_str: str) -> str:
    """Convert ISO date to readable format"""
    try:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_str

def extract_author_institution(author_data: dict) -> tuple:
    """Extract author name and institution from author data"""
    name = author_data.get('name', 'Unknown')
    affiliations = author_data.get('affiliations', [])
    institution = affiliations[0].get('name', 'Unknown') if affiliations else 'Unknown'
    return name, institution 