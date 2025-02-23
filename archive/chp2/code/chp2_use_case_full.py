# Combined Listing for Section 2.5: Full Use Case

import requests
import pandas as pd
import logging
from datetime import datetime, timedelta
import openai

# API keys
NEWS_API_KEY = 'your_news_api_key_here'
openai.api_key = 'your_openai_api_key_here'

# Dynamic date calculation
today = datetime.now().date()
yesterday = today - timedelta(days=1)

# Function to extract articles from NewsAPI
def extract_articles(query, from_date=yesterday, api_key=NEWS_API_KEY):
    url = f'https://newsapi.org/v2/everything?q={query}&from={from_date}&to={today}&apiKey={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        logging.info(f"Successfully extracted {len(articles)} articles.")
        return articles
    else:
        logging.error(f"Failed to fetch articles. Status code: {response.status_code}")
        return None

# Function to preprocess articles
def preprocess_articles(articles):
    data = []
    for article in articles[:5]:  # Limiting to 5 articles for testing
        title = article.get('title', '')
        description = article.get('description', '')
        content = article.get('content', '')
        
        clean_text = f"{title} {description} {content}".replace('\n', ' ').strip()
        data.append({
            'title': title,
            'description': description,
            'content': clean_text
        })
        
    df = pd.DataFrame(data)
    logging.info(f"Preprocessed {len(df)} articles.")
    return df

# Function to perform sentiment analysis
def perform_sentiment_analysis(article_content):
    prompt = f"Analyze the sentiment of the following article content and return 'Positive', 'Neutral', or 'Negative' only: {article_content}."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.5
        )
        
        sentiment = response['choices'][0]['message']['content'].strip()
        return sentiment
    except Exception as e:
        logging.error(f"Error performing sentiment analysis: {e}")
        return None

# Function to update DataFrame with sentiment analysis
def update_with_sentiment(df):
    sentiments = []
    
    for index, content in enumerate(df['content']):
        sentiment = perform_sentiment_analysis(content)
        sentiments.append(sentiment)
        logging.info(f"Processed article {index + 1}/{len(df)}: Sentiment = {sentiment}")
        
    df['sentiment'] = sentiments
    return df

# Workflow Execution
articles = extract_articles('Tesla')
df_articles = preprocess_articles(articles)
df_articles_with_sentiment = update_with_sentiment(df_articles)
print(df_articles_with_sentiment[['title', 'sentiment']])
