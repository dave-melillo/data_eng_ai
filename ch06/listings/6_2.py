import openai
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY") 

# Define a function to detect inconsistencies using Open AI's Chat Completions API Endpoint
def detect_inconsistencies(df):
    discrepancies = {}  #A
    
    # Loop through each column in the DataFrame
    for col in df.columns:  #B
        # Create a prompt to ask Open AI's Chat Completions API Endpoint for inconsistencies in the column
        prompt = f"Identify any inconsistencies in the column '{col}' in this data: {df[col].tolist()}. Note that purchase amount should not be negative for any item."  #C
        
        # Send the prompt to Open AI's Chat Completions API Endpoint and store the response
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )  #D
        
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
