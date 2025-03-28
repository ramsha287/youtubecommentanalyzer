from googleapiclient.discovery import build
import re

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})",
        r"(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]{11})"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None 

def fetch_video_metrics(video_url, api_key):
    """Fetch video engagement metrics (likes, views, etc.)."""
    video_id = extract_video_id(video_url)
    
    if not video_id:
        raise ValueError("Invalid YouTube video URL")
    
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.videos().list(
        part="statistics",
        id=video_id
    )
    response = request.execute()

    if not response.get("items"):
        raise ValueError("No video found for the given URL")
    
    stats = response["items"][0]["statistics"]
    return {
        "views": int(stats.get("viewCount", 0)),
        "likes": int(stats.get("likeCount", 0)),
        "comments": int(stats.get("commentCount", 0))
    }

def fetch_video_comments(video_url, api_key):
    """Fetch comments from a YouTube video."""
    video_id = extract_video_id(video_url)
    
    if not video_id:
        raise ValueError("Invalid YouTube video URL")

    # Explicitly pass the API key to the YouTube API client
    youtube = build("youtube", "v3", developerKey=api_key)

    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        maxResults=100,
        videoId=video_id
    )
    
    while request:
        response = request.execute()
        for item in response.get("items", []):
            comments.append({
                "text": item["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                "is_subscriber": item["snippet"]["topLevelComment"]["snippet"].get("authorIsChannelOwner", False)
            })
        request = youtube.commentThreads().list_next(request, response)
    
    return comments