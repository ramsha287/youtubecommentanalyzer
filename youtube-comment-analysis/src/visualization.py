import streamlit as st
import plotly.express as px
import pandas as pd
import nltk
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter

# Ensure required NLTK datasets are available
nltk.download("stopwords")
nltk.download("punkt")



def create_wordcloud(comments):
    """Generate a word cloud."""
    if not comments:
        return

    text = " ".join([comment.get("cleaned_text", "") for comment in comments if comment.get("cleaned_text")])
    stop_words = set(stopwords.words("english"))
    stop_words.update(["href", "http", "www", "click", "img", "src", "alt"])

    wordcloud = WordCloud(width=800, height=400, background_color="white", stopwords=stop_words, colormap="rainbow").generate(text)
    st.image(wordcloud.to_array(), use_container_width=True)


def create_classification_chart(comments):
    """Create a bar chart showing the distribution of emotions in comments."""
    if not comments:
        return

    def classify_emotion(vader_score):
        compound = vader_score.get("compound", 0)
        if compound >= 0.8:
            return "Excited/Joyful"
        elif 0.4 <= compound < 0.8:
            return "Happy/Positive"
        elif 0.1 <= compound < 0.4 or -0.2 < compound < 0.1:
            return "Neutral"
        elif -0.5 < compound <= -0.2:
            return "Sad"
        elif -0.7 < compound <= -0.5:
            return "Angry"
        elif compound <= -0.7:
            return "Sarcastic"
        return "Neutral"

    emotion_counts = Counter(classify_emotion(comment["vader_sentiment"]) for comment in comments if "vader_sentiment" in comment)
    
    if emotion_counts:
        df_emotions = pd.DataFrame(emotion_counts.items(), columns=['Emotion', 'Count'])
        fig = px.bar(df_emotions, x='Emotion', y='Count', title='Comment Emotion Distribution', color='Emotion')
        st.plotly_chart(fig)


def detect_trending_topics(comments, n_topics=5):
    """Detect and visualize trending topics from comments."""
    if not comments:
        return

    text = [comment.get('cleaned_text', '') for comment in comments if comment.get('cleaned_text')]
    if not text:
        return

    vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
    tfidf_matrix = vectorizer.fit_transform(text)

    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(tfidf_matrix)

    feature_names = vectorizer.get_feature_names_out()
    topics = [{"Topic": f"Topic {idx+1}", "Words": ", ".join([feature_names[i] for i in topic.argsort()[-8:]])} for idx, topic in enumerate(lda.components_)]

    if topics:
        st.write("### Detected Trending Topics")
        st.dataframe(pd.DataFrame(topics))


def create_visualizations(comments):
    """Create sentiment analysis visualizations."""
    if not comments:
        return

    df = pd.DataFrame(comments)

    if "vader_sentiment" not in df.columns or "textblob_sentiment" not in df.columns:
        return

    def classify_sentiment(score):
        return "Positive" if score > 0.05 else "Negative" if score < -0.05 else "Neutral"

    df = df.dropna(subset=["vader_sentiment", "textblob_sentiment"])
    df["sentiment"] = df["vader_sentiment"].apply(lambda x: classify_sentiment(x["compound"]) if isinstance(x, dict) else "Neutral")

    if not df.empty:
        fig = px.scatter(df, 
                         x=df["textblob_sentiment"].apply(lambda x: x["polarity"] if isinstance(x, dict) else 0),
                         y=df["vader_sentiment"].apply(lambda x: x["compound"] if isinstance(x, dict) else 0),
                         color="sentiment", 
                         title="Sentiment Analysis")
        st.plotly_chart(fig)
