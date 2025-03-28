import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# YouTube API Configuration
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# API Settings
MAX_RESULTS = 100
MAX_COMMENTS = 1000

# Text Processing Settings
MIN_WORD_LENGTH = 3
MAX_WORD_LENGTH = 50

# Sentiment Analysis Settings
SENTIMENT_THRESHOLD = 0.1

# Visualization Settings
WORDCLOUD_WIDTH = 800
WORDCLOUD_HEIGHT = 400
PLOT_WIDTH = 800
PLOT_HEIGHT = 400

# File Paths
DATA_DIR = 'data'
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
MODEL_DIR = 'models'

# Logging Configuration
LOG_FILE = 'youtube_comment_analysis.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO' 