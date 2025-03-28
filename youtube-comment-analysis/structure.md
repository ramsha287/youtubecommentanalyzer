📂 youtube-comment-analysis/
│── 📂 src/                     # Source code directory
│   │── 📄 app.py               # Main Streamlit app for user interface
│   │── 📄 get_comments.py      # Fetch comments from YouTube API
│   │── 📄 text_processing.py   # Text cleaning & sentiment analysis
│   │── 📄 classify.py          # Categorize comments (feedback, queries, etc.)
│   │── 📄 visualization.py     # Word cloud & graph generation
│   │── 📄 utils.py            # Helper functions and utilities
│   │── 📄 config.py           # Configuration settings and API keys
│── 📂 models/                  # Trained models directory
│   │── 📄 sentiment_model/     # Sentiment analysis model
│   │── 📄 classifier_model/    # Comment classification model
│── 📂 data/                    # Data storage directory
│   │── 📂 raw/                # Raw comment data
│   │── 📂 processed/          # Processed and analyzed data
│── 📂 tests/                   # Test files directory
│   │── 📄 test_app.py
│   │── 📄 test_processing.py
│── 📄 requirements.txt         # Project dependencies
│── 📄 README.md               # Project documentation
│── 📄 .env                    # Environment variables (API keys)
│── 📄 .gitignore             # Git ignore file

# Project Components Description:

## Core Components:
1. **app.py**
   - Streamlit web interface
   - URL input handling
   - Results display and visualization
   - User interaction management

2. **get_comments.py**
   - YouTube API integration
   - Comment fetching and pagination
   - Rate limiting handling
   - Error management

3. **text_processing.py**
   - Text cleaning and preprocessing
   - Sentiment analysis
   - Language detection
   - Text normalization

4. **classify.py**
   - Comment categorization
   - Topic modeling
   - Intent classification
   - Feedback extraction

5. **visualization.py**
   - Word cloud generation
   - Sentiment distribution plots
   - Category distribution charts
   - Time-based analysis graphs

6. **utils.py**
   - Common utility functions
   - Data validation
   - Error handling
   - Logging setup

7. **config.py**
   - API configurations
   - Model parameters
   - System settings
   - Constants

## Features:
- YouTube video URL input
- Comment extraction and storage
- Sentiment analysis
- Comment categorization (feedback, queries, suggestions, etc.)
- Topic modeling
- Visualization of insights
- Export functionality for reports

## Dependencies:
- streamlit
- google-api-python-client
- pandas
- numpy
- scikit-learn
- nltk
- textblob
- plotly
- wordcloud
- python-dotenv
