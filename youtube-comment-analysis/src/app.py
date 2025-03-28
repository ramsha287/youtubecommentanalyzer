import streamlit as st
from get_comments import fetch_video_comments, fetch_video_metrics
from text_processing import process_comments
from classify import categorize_comments
from visualization import create_visualizations, create_wordcloud, create_classification_chart,detect_trending_topics
from config import YOUTUBE_API_KEY
from topic_modeling import cluster_comments
import pandas as pd


def main():
    st.title("YouTube Comment Analysis")
    st.write("Analyze comments from any YouTube video")

    # Input: YouTube Video URL
    video_url = st.text_input("Enter YouTube Video URL:", "")

    if st.button("Analyze Video"):
        if not video_url:
            st.error("Please enter a valid YouTube URL.")
        else:
            try:
                # Fetch video metrics
                metrics = fetch_video_metrics(video_url, YOUTUBE_API_KEY)
                if metrics:
                    st.subheader("📊 Video Engagement Metrics")
                    st.write(f"**Views:** {metrics.get('views', 'N/A')}")
                    st.write(f"**Likes:** {metrics.get('likes', 'N/A')}")
                    st.write(f"**Comments:** {metrics.get('comments', 'N/A')}")
                else:
                    st.warning("Failed to retrieve video metrics.")

                # Fetch comments
                st.subheader("💬 Fetching Comments...")
                comments = fetch_video_comments(video_url, YOUTUBE_API_KEY)
                if not comments:
                    st.warning("No comments found on this video.")
                    return

                # Process and categorize comments
                processed_comments = process_comments(comments)
                categorized_comments = categorize_comments(processed_comments)

                # Generate visualizations
                st.subheader("📊 Comment Analysis Visualization")
                create_visualizations(categorized_comments)

                #top trending topics
                st.subheader("🔍 Trending Topics")
                detect_trending_topics(processed_comments)
                

                # Create word cloud
                st.subheader("☁️ Word Cloud")
                create_wordcloud(processed_comments)

                # Create classification chart
                st.subheader("📊 Comment Classification Chart")
                create_classification_chart(processed_comments)

                # Cluster comments using topic modeling
                st.subheader("🔍 Topic Clustering")
                clusters = cluster_comments(processed_comments)
                st.write(clusters)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
