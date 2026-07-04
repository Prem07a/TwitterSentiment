    # app.py
import streamlit as st
import joblib
import plotly.graph_objects as go

from xquik_export import normalize_xquik_csv


st.set_page_config(page_title="Twitter Sentiment", page_icon="./image/tweet.png")


@st.cache_resource
def set_models():
    model = joblib.load("./models/bestSentiment_css.pkl")
    vectorizer = joblib.load("./models/vectorizer_css.pkl")
    return model, vectorizer


def predict_sentiment_values(text):
    input_data = [text]
    model, vectorizer = set_models()
    processed_data = vectorizer.transform(input_data)

    prediction = model.predict_proba(processed_data)[0]

    labels = ["Negative", "Positive"]
    values = list(prediction)
    if round(max(values),2) >= .75: 
        if values[0] > values[1]:
            values = [1,0]
        else:
            values = [0,1]
    else:
        values = [.5,.5]

    if values[0] == 0.5:
        sentiment = "Neutral"
    else:
        sentiment = labels[0] if values[0] > values[1] else labels[1]

    return sentiment, labels, values


def predict_sentiment(text):
    sentiment, labels, values = predict_sentiment_values(text)

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.5,
                marker=dict(colors=["red", "green"]),
                domain=dict(x=[0.2, 0.8], y=[0.2, 0.8]),
            )
        ]
    )

    st.sidebar.plotly_chart(fig)

    return sentiment


def twitter_sentiment_analysis():
    col1, col2 = st.columns([1, 4])

    with col1:
        st.image("./image/tweet.png", width=150)
    with col2:
        st.title("Twitter Sentiment Analysis")

    st.image("./image/analysis_ratio.png")

    with open("./Analysis/analysis_ratio.md", "r") as f:
        st.markdown(f.read())

    st.image("./image/weekday__time_ratio.png")

    with open("./Analysis/weekday_time_ratio.md", "r") as f:
        st.markdown(f.read())

    st.image("./image/neg_posneg_ratio.png")

    with open("./Analysis/neg_posneg_ratio.md", "r") as f:
        st.markdown(f.read())

    st.image("./image/tweet_trend.png")
    with open("./Analysis/tweet_trend.md", "r") as f:
        st.markdown(f.read())


def sentiment_check():
    col1, col2 = st.columns([1, 4])

    with col1:
        st.image("./image/tweet.png", width=150)
    with col2:
        st.title("Sentiment Check")

    user_text = st.text_area("Enter text for sentiment check:", placeholder="@tweet")
    xquik_file = st.file_uploader("Upload a saved Xquik CSV export", type=["csv"])

    if xquik_file is not None:
        try:
            rows = normalize_xquik_csv(xquik_file.getvalue().decode("utf-8-sig"))
        except ValueError as exc:
            st.error(str(exc))
        else:
            if rows:
                analyzed_rows = []
                for row in rows[:100]:
                    sentiment, _, _ = predict_sentiment_values(row["text"])
                    analyzed_rows.append({**row, "sentiment": sentiment})
                st.success(f"Analyzed {len(analyzed_rows)} Xquik export rows.")
                st.dataframe(analyzed_rows, use_container_width=True)
            else:
                st.warning("No non-empty tweet text rows found in the Xquik export.")

    if st.button("Tweet", key="tweet_button", help="Click to analyze sentiment."):
        if user_text.strip():
            sentiment_result = predict_sentiment(user_text)

            if sentiment_result == "Positive":
                st.success("Predicted Sentiment: Positive")
            elif sentiment_result == "Neutral":
                st.warning("Predicted Sentiment: Neutral")
            else:
                st.error("Predicted Sentiment: Negative")

        else:
            st.warning("Please do not leave the input text box empty.")


menu = ["Tweet Check", "Analysis"]
choice = st.sidebar.selectbox("Select Page", menu)

if choice == "Analysis":
    twitter_sentiment_analysis()
elif choice == "Tweet Check":
    sentiment_check()
