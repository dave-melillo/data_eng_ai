# Listing 2: Extract Articles from NewsAPI
import requests
import pandas as pd
import logging
from datetime import datetime, timedelta

NEWS_API_KEY = 'your_news_api_key_here'

today = datetime.now().date()
yesterday = today - timedelta(days=1)

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

articles = extract_articles('Tesla')
