# app.py
import streamlit as st
import streamlit.components.v1 as components
import joblib
import base64

model = joblib.load('./models/bestSentiment_css.pkl')
vectorizer = joblib.load('./models/vectorizer_css.pkl')
st.set_page_config(page_title="Twitter Sentiment")

def predict_sentiment(text):
    
    input_data = [text]

    # Apply the saved CountVectorizer
    processed_data = vectorizer.transform(input_data)

    prediction = model.predict(processed_data)
   
    return prediction[0]

# Define the pages
def twitter_sentiment_analysis():
    st.title("Twitter Sentiment Analysis")
    # Opening file from file path
    with open('./SentimentAnalysis.html', "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)
    
def sentiment_check():
    st.image('./image/tweet.png', width=150)
    st.title("Sentiment Check")

    user_text = st.text_area("Enter text for sentiment check:", placeholder='@tweet')

    tweet_button = st.button("Tweet", key="tweet_button", help="Click to analyze sentiment with Twitter logo")
    if tweet_button:
        sentiment_result = predict_sentiment(user_text)
        
        if sentiment_result == "Positive":
            sentiment_color = "green"
        else:
            sentiment_color = "red"

        styled_text = f'<div style="background-color: {sentiment_color}; padding: 10px; border-radius: 5px;">Predicted Sentiment: {sentiment_result}</div>'
        st.markdown(styled_text, unsafe_allow_html=True)

menu = [ "Tweet Check", "Analysis"]
choice = st.sidebar.selectbox("Select Page", menu)

if choice == "Analysis":
    twitter_sentiment_analysis()
elif choice == "Tweet Check":
    sentiment_check()
