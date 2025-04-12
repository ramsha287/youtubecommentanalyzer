# YouTube Comment Analysis

A powerful tool for analyzing YouTube video comments using natural language processing and machine learning techniques.

## Features

- Fetch comments from any YouTube video
- Sentiment analysis of comments
- Comment categorization (feedback, queries, suggestions, etc.)
- Word cloud visualization
- Interactive visualizations using Plotly
- Export functionality for analysis results

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/youtube-comment-analysis.git
cd youtube-comment-analysis
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Copy `.env.example` to `.env`
- Add your YouTube API key to the `.env` file

## Usage

1. Start the Streamlit app:
```bash
streamlit run src/app.py
```

2. Enter a YouTube video URL in the input field

3. Click "Analyze Comments" to start the analysis

4. View the results and visualizations



## Requirements

- Python 3.8+
- YouTube Data API v3 key
- See requirements.txt for Python package dependencies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
