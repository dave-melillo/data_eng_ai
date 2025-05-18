def perform_sentiment_analysis(article_content):  
    prompt = f"Analyze the sentiment of the following article content and return 'Positive', 'Neutral', or 'Negative' only: {article_content}."  #A
    
    try:  
        response = openai.chat.completions.create(  
            model="gpt-4o",  
            messages=[  
                {"role": "system", "content": "You are a helpful assistant."},  
                {"role": "user", "content": prompt}  
            ],  
            max_tokens=50,  
            temperature=0.5  
        )  
        
        sentiment = response.choices[0].message.content.strip()  #B  
        return sentiment  
    
    except Exception as e:  
        logging.error(f"Error performing sentiment analysis: {e}")  
        return None  

#A Modify the prompt to return only a structured sentiment value.
#B Extract and clean the AI's response for structured output.
