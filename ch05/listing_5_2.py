# Function to preprocess articles  
def preprocess_articles(articles):  
    data = []  #A
    
    for article in articles[:5]:  # Limit to 5 articles for testing  #B
        title = article.get('title', '')  
        description = article.get('description', '')  
        content = article.get('content', '')  
        
        # Clean and format the text  
        clean_text = f"{title} {description} {content}".replace('\n', ' ').strip()  #C
        data.append({  
            'title': title,  
            'description': description,  
            'content': clean_text  
        })  
        
    df = pd.DataFrame(data)  #D
    logging.info(f"Preprocessed {len(df)} articles.")  
    return df  

# Preprocess the extracted articles  
df_articles = preprocess_articles(articles)  #E

#A Initialize an empty list to store preprocessed article data.
#B Loop through the first 5 articles, limiting scope for testing.
#C Clean and format the combined text fields by removing line breaks.
#D Convert the list of dictionaries into a DataFrame for structured analysis.
#E Call preprocess_articles and store the result in df_articles.
