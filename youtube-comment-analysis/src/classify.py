from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

def categorize_comments(comments):
    """Categorize comments based on sentiment."""
    categorized_comments = []
    for comment in comments:
        vader_sentiment = comment.get("vader_sentiment", {})
        compound_score = vader_sentiment.get("compound", 0)

        if compound_score > 0.05:
            category = "Positive"
        elif compound_score < -0.05:
            category = "Negative"
        else:
            category = "Neutral"

        comment["category"] = category
        categorized_comments.append(comment)

    return categorized_comments