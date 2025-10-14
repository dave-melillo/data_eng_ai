#### **Listing 5.1: Extracting News Articles**
```python
import requests  #A
import pandas as pd  
import logging  
from datetime import datetime, timedelta  

NEWS_API_KEY = 'your_news_api_key_here'  #B

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
        return None  

# Example use case  
articles = extract_articles('Tesla')  #F

#A Import required libraries for requests, data handling, and logging.
#B Store your NewsAPI key as a constant for easy access.
#C Calculate today’s date and set yesterday for the date range.
#D Construct the URL for the NewsAPI request using query, date range, and API key.
#E Extract articles from the response and log success or failure.
#F Call the function with "Tesla" as a query example.