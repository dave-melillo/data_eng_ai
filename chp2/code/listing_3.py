# Listing 3: Preprocess Articles
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

df_articles = preprocess_articles(articles)
