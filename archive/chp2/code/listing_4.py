# Listing 4: Initial Sentiment Analysis Function
import openai

openai.api_key = 'your_openai_api_key_here'

def perform_sentiment_analysis(article_content):
    prompt = f"Analyze the sentiment of the following article content: {article_content}. Is the sentiment positive, negative, or neutral?"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.5
        )
        
        sentiment = response['choices'][0]['message']['content'].strip()
        return sentiment
    except Exception as e:
        logging.error(f"Error performing sentiment analysis: {e}")
        return None

example_article_content = df_articles['content'].iloc[0]
sentiment = perform_sentiment_analysis(example_article_content)
print(f"Sentiment: {sentiment}")
