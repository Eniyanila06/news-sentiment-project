import pandas as pd
from collections import Counter
from text_to_speech import generate_hindi_speech

def comparative_sentiment_analysis(company_name):
    csv_file = f"{company_name}_news_with_sentiment.csv"
    
    try:
        df = pd.read_csv(csv_file)

        # Handle missing or NaN values
        df["title"] = df["title"].fillna("Unknown Article")
        df["summary"] = df["summary"].fillna("No summary available")
        df["sentiment"] = df["sentiment"].fillna("Neutral")

        # Count occurrences of each sentiment category
        sentiment_counts = Counter(df["sentiment"])

        # Comparative Sentiment Report
        comparative_report = {
            "Company": company_name,
            "Sentiment Distribution": {
                "Positive": sentiment_counts.get("Positive", 0),
                "Negative": sentiment_counts.get("Negative", 0),
                "Neutral": sentiment_counts.get("Neutral", 0)
            },
            "Coverage Differences": [],
            "Topic Overlap": {
                "Common Topics": set(),
                "Unique Topics": {}
            }
        }

        # Identify Topic Overlap & Differences
        topics_dict = {}
        for _, row in df.iterrows():
            title = row["title"]
            topics = set(row.get("topics", "").split(", ")) if isinstance(row.get("topics"), str) else set()
            topics_dict[title] = topics
            comparative_report["Topic Overlap"]["Common Topics"].update(topics)

        for title, topics in topics_dict.items():
            unique_topics = topics - comparative_report["Topic Overlap"]["Common Topics"]
            comparative_report["Topic Overlap"]["Unique Topics"][title] = list(unique_topics)

        # Generate Summary for TTS
        final_summary = f"""{company_name} की नवीनतम खबरें इस प्रकार हैं। 
        सकारात्मक खबरें: {sentiment_counts.get('Positive', 0)}, 
        नकारात्मक खबरें: {sentiment_counts.get('Negative', 0)}, 
        तटस्थ खबरें: {sentiment_counts.get('Neutral', 0)}।"""

        # Convert summary to Hindi speech
        output_audio = f"{company_name}_summary.mp3"
        generate_hindi_speech(final_summary, output_audio)

        return comparative_report

    except FileNotFoundError:
        print("Sentiment CSV file not found! Please run sentiment_analysis.py first.")
        return None

# Example Usage
if __name__ == "__main__":
    company_name = input("Enter the company name: ")
    result = comparative_sentiment_analysis(company_name)
    if result:
        print("Comparative Analysis Completed Successfully!")
        print(result)


