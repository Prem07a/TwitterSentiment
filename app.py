    # app.py
import streamlit as st
import joblib
import plotly.graph_objects as go


st.set_page_config(page_title="Twitter Sentiment", page_icon="./image/tweet.png")


@st.cache_resource
def set_models():
    model = joblib.load("./models/bestSentiment_css.pkl")
    vectorizer = joblib.load("./models/vectorizer_css.pkl")
    return model, vectorizer


def predict_sentiment(text):
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
    
    if values[0] == 0.5:
        return "Neutral"
    return labels[0] if values[0] > values[1] else labels[1]


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


menu = ["Tweet Check", "Analysis"]
choice = st.sidebar.selectbox("Select Page", menu)

if choice == "Analysis":
    twitter_sentiment_analysis()
elif choice == "Tweet Check":
    sentiment_check()
