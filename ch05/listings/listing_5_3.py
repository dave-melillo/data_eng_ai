import os
from openai import OpenAI

# Create the OpenAI client
client = OpenAI()  #A
MODEL_MAIN = os.getenv("DEAI_MODEL_MAIN", "gpt-5.5")       # frontier model: extraction, hard reasoning
MODEL_MINI = os.getenv("DEAI_MODEL_MINI", "gpt-5.4-mini")  # cheaper model: ranking, triage, high volume

# Function to perform sentiment analysis using ChatGPT  
def perform_sentiment_analysis(article_content):  
    prompt = f"Analyze the sentiment of the following article content: {article_content}. Is the sentiment positive, negative, or neutral?"
    
    try:  
        response = client.chat.completions.create(  
            model=MODEL_MAIN,  
            messages=[  
                {"role": "system", "content": "You are a helpful assistant."},  
                {"role": "user", "content": prompt}  
            ],  
            max_completion_tokens=100,  
            temperature=0.5  
        )
        
        sentiment = response.choices[0].message.content.strip()  #B
        return sentiment  
    
    except Exception as e:  
        logging.error(f"Error performing sentiment analysis: {e}")  
        return None  

# Example use case  
example_article_content = df_articles['combined_text'].iloc[0]  #C
sentiment = perform_sentiment_analysis(example_article_content)  #D
print(f"Sentiment: {sentiment}")  #E

#A Create the client; it reads OPENAI_API_KEY from the environment.
#B Extract and clean the response to obtain the sentiment result.
#C Select the content of the first article for analysis.
#D Call the perform_sentiment_analysis function on sample text.
#E Print the sentiment result to verify output.
