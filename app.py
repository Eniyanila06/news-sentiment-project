import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from sentiment_analysis import analyze_sentiment
from comparative_analysis import comparative_sentiment_analysis

import streamlit as st
import pandas as pd
from sentiment_analysis import analyze_sentiment
from comparative_analysis import comparative_sentiment_analysis
from text_to_speech import generate_hindi_speech
import os

# Streamlit UI
st.title("📰 News Sentiment Analysis")
st.write("Analyze the sentiment of news articles related to a company.")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Load data
    df = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data Preview:")
    st.write(df.head())

    # Input company name
    company_name = st.text_input("Enter the company name:", "Tesla")

    if st.button("Analyze Sentiment"):
        # Perform sentiment analysis
        analyze_sentiment(company_name)

        # Perform comparative analysis
        summary = comparative_sentiment_analysis(company_name)
        st.write("### Sentiment Summary:")
        st.write(summary)

        # Convert to Hindi speech
        speech_filename = f"{company_name}_summary.mp3"
        generate_hindi_speech(summary, speech_filename)

        # Play audio
        st.audio(speech_filename)

        # Show success message
        st.success("Analysis & Speech generation completed! 🎉")
