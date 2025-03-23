from transformers import pipeline
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load Pretrained Sentiment Analysis Model
sentiment_model = pipeline("sentiment-analysis")
sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

vader_analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Analyze the sentiment of a given text using two models:
    1. Hugging Face Transformer model
    2. Vader Sentiment Analyzer

    Parameters:
    text (str): The news article summary.

    Returns:
    str: Sentiment category (Positive, Negative, Neutral).
    """
    sentiment_result = sentiment_model(text)
    return sentiment_result
    
    # Transformer-based Sentiment Analysis
    transformer_result = sentiment_pipeline(text[:512])  # Limiting to 512 chars
    transformer_label = transformer_result[0]['label']

    # Vader-based Sentiment Analysis
    vader_scores = vader_analyzer.polarity_scores(text)
    vader_compound = vader_scores['compound']

    # Determine final sentiment
    if transformer_label == "POSITIVE" and vader_compound > 0.05:
        return "Positive"
    elif transformer_label == "NEGATIVE" and vader_compound < -0.05:
        return "Negative"
    else:
        return "Neutral"

if __name__ == "__main__":
    # Load extracted news articles
    company_name = input("Enter company name (same as CSV filename): ")
    csv_file = f"{company_name}_news.csv"

    try:
        df = pd.read_csv(csv_file)
        df["sentiment"] = df["summary"].apply(analyze_sentiment)  # Apply sentiment analysis
        df.to_csv(f"{company_name}_news_with_sentiment.csv", index=False)  # Save new file
        
        print(df)
        print(f"Sentiment analysis saved in {company_name}_news_with_sentiment.csv")

    except FileNotFoundError:
        print("News CSV file not found! Please run news_extractor.py first.")
