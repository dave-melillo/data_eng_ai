import openai
import pandas as pd

# Function to detect inconsistencies using AI
def detect_inconsistencies(df):
    discrepancies = {}  #A

    for col in df.columns:  #B
        prompt = f"Identify inconsistencies in the '{col}' column: {df[col].tolist()}. Ensure purchase amounts are non-negative."  #C
        
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )  #D
        
        discrepancies[col] = response['choices'][0]['message']['content']  #E

    return discrepancies  #F

# Create a sample DataFrame
df = pd.DataFrame({
    'email': ['user1@example.com', 'user2@.com', '555-1234', 'user4@example.com'],
    'age': [25, None, 30, 40],
    'purchase_amount': [100.5, -50.0, None, 200.0]
})

# Detect inconsistencies
discrepancies = detect_inconsistencies(df)  #J
print("Detected Inconsistencies:", discrepancies)  #K
