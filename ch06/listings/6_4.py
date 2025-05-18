import pandas as pd
import openai
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the response structure
class CleanedData(BaseModel):
    duplicates: List[int]
    drop_columns: List[str]

# Sample DataFrame
df = pd.DataFrame({
    'customer_id': [1, 2, 2, 3, 3],
    'preferred_store_location': ['NY', 'CA', 'CA', 'TX', None],
    'purchase_amount': [200, 300, 300, 400, 400],
    'optional_note': [None, None, None, None, None]
})

# Format the dataset
records = df.to_dict(orient="records")

# Prompt
prompt = (
    "You are a data cleaning assistant. Review the dataset and return the following:\n"
    "- A list of row indexes that are exact duplicates based on values.\n"
    "- A list of column names that contain more than 50% null values and should be dropped.\n"
    "Respond with only the required data for cleaning."
)

# Completion call with response_format
completion = openai.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": str(records)}
    ],
    response_format=CleanedData
)

# Extract structured output
cleaning_info = completion.choices[0].message.parsed

# Apply cleaning
df_cleaned = df.drop(index=cleaning_info.duplicates)
df_cleaned = df_cleaned.drop(columns=cleaning_info.drop_columns, errors='ignore')

# Show cleaned output
print(df_cleaned)
