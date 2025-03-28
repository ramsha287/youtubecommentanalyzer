import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def cluster_comments(comments, n_topics=5):
    """Cluster comments into topics and visualize with Streamlit."""
    text = [comment['cleaned_text'] for comment in comments if comment['cleaned_text']]

    if not text:
        st.warning("No valid text available for topic detection.")
        return

    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(text)

    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(tfidf_matrix)

    topics = []
    for idx, topic in enumerate(lda.components_):
        top_words = [vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]]
        topics.append({"Topic": f"Topic {idx + 1}", "Keywords": ", ".join(top_words)})

    df_topics = pd.DataFrame(topics)

    # Display topics in a nice format
    st.subheader("🔍 Discovered Topics")
    st.dataframe(df_topics)

    # Show example comments for each topic
    st.subheader("📝 Example Comments for Topics")
    for idx, topic in enumerate(df_topics["Topic"]):
        st.markdown(f"**{topic}** - *Keywords: {df_topics.iloc[idx]['Keywords']}*")
        st.write(f"Example: *{text[idx][:200]}...*")
