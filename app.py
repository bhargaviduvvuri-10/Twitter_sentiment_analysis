import streamlit as st
import tweepy
import pandas as pd
import re
from textblob import TextBlob

# ---- Configuration ----
# Paste your Twitter API credentials here:
bearer_token = "AAAAAAAAAAAAAAAAAAAAANdM2wEAAAAAZiYXJQDyMyizC9%2B0P9A3gTJLcE8%3DKZMdFICmFBIQxg0gI6LROFM6co27T6zBTysKDahbTAk8DR9Id5"
consumer_key = "Hcx1r2JpF3dDJJJ9HUJn9tJwg"
consumer_secret = "ACnzuk9fOqzyjHmFsbUdDfIlu8T7avXloQQsIGpJEzpfa36PNH"
access_token = "1833530663200559109-kkxS5fJrOTFl7GRoqJMJH5RJKhUKYQ"
access_token_secret = "aVCA5R8oBoHO1khZsCw80LnK8UFSjhsUAJrbXFnmlWazM"

# ---- Authentication ----
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    wait_on_rate_limit=True
)

# ---- Helper functions ----
def clean_text(text):
    text = re.sub(r'http\S+|@\S+|#', '', text)
    text = re.sub(r'[^A-Za-z\s]', '', text)
    return text.lower().strip()

def get_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0: return "Positive"
    if polarity < 0: return "Negative"
    return "Neutral"

# ---- Streamlit UI ----
st.title("Live Twitter Sentiment Analyzer")
st.write("Enter a hashtag or keyword to fetch live tweets and analyze their sentiment.")

query = st.text_input("Keyword or hashtag", "#AI")
count = st.slider("Number of tweets to fetch", 10, 100, 50)

if st.button("Analyze"):
    with st.spinner("Fetching tweets…"):
        resp = client.search_recent_tweets(query=f"{query} lang:en", max_results=count)
    tweets = resp.data or []
    if not tweets:
        st.write("No tweets found. Try another query.")
    else:
        data = []
        for t in tweets:
            raw = t.text
            clean = clean_text(raw)
            sentiment = get_sentiment(clean if clean else raw)
            data.append({"Tweet": raw, "Sentiment": sentiment})
        df = pd.DataFrame(data)
        st.dataframe(df)

        # Show sentiment counts
        counts = df["Sentiment"].value_counts()
        st.bar_chart(counts)
