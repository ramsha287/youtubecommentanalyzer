import logging
from datetime import datetime
import os
import json
import re

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('youtube_comment_analysis.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def validate_youtube_url(url):
    """Validate YouTube URL format."""
    youtube_pattern = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]{11}$'
    return bool(re.match(youtube_pattern, url))

def save_comments_to_file(comments, filename=None):
    """Save comments to a JSON file."""
    if filename is None:
        filename = f'comments_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    try:
        with open(os.path.join('data/raw', filename), 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logging.error(f"Error saving comments to file: {str(e)}")
        return False

def load_comments_from_file(filename):
    """Load comments from a JSON file."""
    try:
        with open(os.path.join('data/raw', filename), 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading comments from file: {str(e)}")
        return None 