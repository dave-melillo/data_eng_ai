import openai  

# Set your OpenAI API key  
openai.api_key = 'your_openai_api_key_here'  #A

# Function to perform sentiment analysis using ChatGPT  
def perform_sentiment_analysis(article_content):  
    prompt = f"Analyze the sentiment of the following article content: {article_content}. Is the sentiment positive, negative, or neutral?"
    
    try:  
        response = openai.chat.completions.create(  
            model="gpt-4o",  
            messages=[  
                {"role": "system", "content": "You are a helpful assistant."},  
                {"role": "user", "content": prompt}  
            ],  
            max_tokens=100,  
            temperature=0.5  
        )
        
        sentiment = response.choices[0].message.content.strip()  #B
        return sentiment  
    
    except Exception as e:  
        logging.error(f"Error performing sentiment analysis: {e}")  
        return None  

# Example use case  
example_article_content = df_articles['content'].iloc[0]  #C
sentiment = perform_sentiment_analysis(example_article_content)  #D
print(f"Sentiment: {sentiment}")  #E

#A Authenticate with OpenAI using the API key.
#B Extract and clean the response to obtain the sentiment result.
#C Select the content of the first article for analysis.
#D Call the perform_sentiment_analysis function on sample text.
#E Print the sentiment result to verify output.
