import os
import re
import logging
import nltk
from googleapiclient.discovery import build
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Ensure required NLTK resources are downloaded
nltk_data_dir = os.path.join(os.getcwd(), 'nltk_data')
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)
nltk.data.path.append(nltk_data_dir)

nltk.download('punkt', download_dir=nltk_data_dir)
nltk.download('stopwords', download_dir=nltk_data_dir)
nltk.download('vader_lexicon', download_dir=nltk_data_dir)

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Load stopwords once globally
STOP_WORDS = set(stopwords.words("english"))

def clean_text(text):
    """Clean and normalize text by removing links, punctuation, and numbers."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r"<.*?>", "", text)  # Remove HTML tags
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    text = re.sub(r"\d+", "", text)  # Remove numbers
    text = " ".join(text.split())  # Normalize spaces
    return text

def process_comments(comments):
    """Process comments: clean text, tokenize, remove stopwords, and analyze sentiment."""
    processed_comments = []
    
    for comment in comments:
        text = comment.get("text", "")
        if not isinstance(text, str):
            continue

        # Clean the text
        cleaned_text = clean_text(text)

        # Tokenize and remove stopwords
        tokens = word_tokenize(cleaned_text)
        tokens = [token for token in tokens if token not in STOP_WORDS]

        # Sentiment analysis
        textblob_sentiment = TextBlob(cleaned_text).sentiment._asdict()
        vader_sentiment = sia.polarity_scores(cleaned_text)

        # Add processed data
        processed_comments.append({
            "original_text": text,
            "cleaned_text": cleaned_text,
            "tokens": tokens,
            "textblob_sentiment": textblob_sentiment,
            "vader_sentiment": vader_sentiment,
            "is_subscriber": comment.get("is_subscriber", False)
        })

    return processed_comments

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})",  # Standard URL
        r"(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]{11})"  # Shortened URL
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube video URL")

def fetch_video_comments(video_url, api_key):
    """Fetch comments from a YouTube video."""
    video_id = extract_video_id(video_url)
    
    if not video_id:
        raise ValueError("Invalid YouTube video URL")

    youtube = build("youtube", "v3", developerKey=api_key)
    comments = []
    
    request = youtube.commentThreads().list(
        part="snippet",
        maxResults=100,
        videoId=video_id
    )

    while request:
        try:
            response = request.execute()
            for item in response.get("items", []):
                comments.append({
                    "video_id": video_id,
                    "text": item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                    "is_subscriber": item["snippet"]["topLevelComment"]["snippet"].get("authorIsChannelOwner", False)
                })
            request = youtube.commentThreads().list_next(request, response)
        except Exception as e:
            logging.error(f"Error fetching comments: {e}")
            break

    return comments

if __name__ == "__main__":
    # Secure API Key Retrieval
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    if not YOUTUBE_API_KEY:
        logging.error("YouTube API key is missing. Set it as an environment variable: 'YOUTUBE_API_KEY'")
        exit(1)

    # Replace with your YouTube video URL
    video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"

    logging.info("Fetching YouTube comments...")
    comments = fetch_video_comments(video_url, YOUTUBE_API_KEY)

    if comments:
        logging.info(f"Fetched {len(comments)} comments. Processing...")
        processed_comments = process_comments(comments)

        logging.info("Processed comments:")
        for comment in processed_comments[:5]:  # Print first 5 comments for preview
            print(comment)
    else:
        logging.warning("No comments found for this video.")
