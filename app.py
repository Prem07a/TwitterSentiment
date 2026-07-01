    # app.py
import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go


st.set_page_config(page_title="Twitter Sentiment", page_icon="./image/tweet.png")


@st.cache_resource
def set_models():
    model = joblib.load("./models/bestSentiment_css.pkl")
    vectorizer = joblib.load("./models/vectorizer_css.pkl")
    return model, vectorizer


TEXT_COLUMN_CANDIDATES = [
    "tweet",
    "text",
    "content",
    "message",
    "body",
    "post",
    "comment",
    "review",
]


def detect_text_column(columns):
    normalized_columns = {str(column).strip().lower(): column for column in columns}
    for candidate in TEXT_COLUMN_CANDIDATES:
        if candidate in normalized_columns:
            return normalized_columns[candidate]
    return columns[0] if len(columns) > 0 else None


def score_text(text):
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

    return sentiment, values


def render_sentiment_chart(values):
    labels = ["Negative", "Positive"]
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


def predict_sentiment(text):
    sentiment, values = score_text(text)
    render_sentiment_chart(values)
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

    st.subheader("Batch CSV Sentiment")
    uploaded_file = st.file_uploader(
        "Upload a CSV with tweet, text, content, message, body, post, comment, or review text",
        type=["csv"]
    )

    if uploaded_file is not None:
        batch_df = pd.read_csv(uploaded_file)
        detected_column = detect_text_column(batch_df.columns)

        if detected_column is None:
            st.warning("Upload a CSV with at least one text column.")
            return

        text_column = st.selectbox(
            "Text column",
            batch_df.columns,
            index=list(batch_df.columns).index(detected_column)
        )
        usable_rows = batch_df[batch_df[text_column].astype(str).str.strip() != ""].copy()

        if usable_rows.empty:
            st.warning("No non-empty text rows were found.")
            return

        if st.button("Analyze CSV", key="batch_csv_button"):
            predictions = []
            for text in usable_rows[text_column].astype(str):
                sentiment, values = score_text(text)
                predictions.append({
                    "predicted_sentiment": sentiment,
                    "negative_score": values[0],
                    "positive_score": values[1],
                })

            results_df = usable_rows.copy()
            predictions_df = pd.DataFrame(predictions, index=usable_rows.index)
            for column in predictions_df.columns:
                results_df[column] = predictions_df[column]
            st.dataframe(results_df.head(25), use_container_width=True)
            st.download_button(
                "Download predictions",
                results_df.to_csv(index=False).encode("utf-8"),
                "twitter_sentiment_predictions.csv",
                "text/csv",
                key="download_batch_csv"
            )


menu = ["Tweet Check", "Analysis"]
choice = st.sidebar.selectbox("Select Page", menu)

if choice == "Analysis":
    twitter_sentiment_analysis()
elif choice == "Tweet Check":
    sentiment_check()
