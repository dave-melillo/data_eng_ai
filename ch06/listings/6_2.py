import logging
from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()  # reads OPENAI_API_KEY from the environment
MODEL_MAIN = os.getenv("DEAI_MODEL_MAIN", "gpt-5.5")       # frontier model: extraction, hard reasoning
MODEL_MINI = os.getenv("DEAI_MODEL_MINI", "gpt-5.4-mini")  # cheaper model: ranking, triage, high volume

# Define a function to detect inconsistencies using Open AI's Chat Completions API Endpoint
def detect_inconsistencies(df):
    discrepancies = {}  #A
    
    # Loop through each column in the DataFrame
    for col in df.columns:  #B
        # Create a prompt to ask Open AI's Chat Completions API Endpoint for inconsistencies in the column
        prompt = f"Identify any inconsistencies in the column '{col}' in this data: {df[col].tolist()}. Note that purchase amount should not be negative for any item."  #C
        
        # Send the prompt to Open AI's Chat Completions API Endpoint and store the response
        try:
            response = client.chat.completions.create(
                model=MODEL_MAIN,
                messages=[{"role": "user", "content": prompt}]
            )  #D
        except Exception as e:
            logging.error(f"API error for column '{col}': {e}")
            continue
        
        # Save the response for the column
        discrepancies[col] = response.choices[0].message.content.strip() #E
    
    return discrepancies  #F

# Create a sample DataFrame with inconsistent data
df = pd.DataFrame({
    'email': ['user1@example.com', 'user2@.com', '555-1234', 'user4@example.com'],  #G
    'age': [25, None, 30, 40],  #H
    'purchase_amount': [100.5, -50.0, None, 200.0]  #I
})

# Use the function to detect inconsistencies with AI assistance
discrepancies = detect_inconsistencies(df)  #J

# Output the detected inconsistencies
print("Detected Inconsistencies:", discrepancies)  #K
