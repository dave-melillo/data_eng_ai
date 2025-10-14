#cell 1
import requests  #A
import pandas as pd  
import logging  
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta  
pd.set_option("display.max_colwidth", None)

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")  #B

# Dynamic date calculation: today minus one day  
today = datetime.now().date()  #C  
yesterday = today - timedelta(days=1)  

# Function to extract articles from NewsAPI  
def extract_articles(query, from_date=yesterday, api_key=NEWS_API_KEY):  
    url = f'https://newsapi.org/v2/everything?q={query}&from={from_date}&to={today}&apiKey={api_key}'  #D
    response = requests.get(url)  
    
    if response.status_code == 200:  
        articles = response.json().get('articles', [])  #E
        logging.info(f"Successfully extracted {len(articles)} articles.")  
        return articles  
    else:  
        logging.error(f"Failed to fetch articles. Status code: {response.status_code}")  
        return []  

# Example use case  
articles = extract_articles('Tesla')  #F

# Build a DataFrame with one row per article and full JSON blob
df = pd.DataFrame({'article': articles})  #G
df

