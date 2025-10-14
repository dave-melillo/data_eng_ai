# Listing 5: Update DataFrame with Sentiment Analysis Results
def update_with_sentiment(df):
    sentiments = []
    
    for index, content in enumerate(df['content']):
        sentiment = perform_sentiment_analysis(content)
        sentiments.append(sentiment)
        logging.info(f"Processed article {index + 1}/{len(df)}: Sentiment = {sentiment}")
        
    df['sentiment'] = sentiments
    return df

df_articles_with_sentiment = update_with_sentiment(df_articles)
print(df_articles_with_sentiment[['title', 'sentiment']])
