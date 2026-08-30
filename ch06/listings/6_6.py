import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional

load_dotenv()
client = OpenAI()  # reads OPENAI_API_KEY from the environment
MODEL_MAIN = os.getenv("DEAI_MODEL_MAIN", "gpt-5.5")       # frontier model: extraction, hard reasoning
MODEL_MINI = os.getenv("DEAI_MODEL_MINI", "gpt-5.4-mini")  # cheaper model: ranking, triage, high volume

# Define the structured response format  #A
class StandardizationInstructions(BaseModel):  #B
    normalized_dates: List[str]                #C
    cleaned_skus: List[Optional[str]]          #D
    truncated_descriptions: List[str]          #E
    full_names: List[str]                      #F
    mapped_categories: List[str]               #G

# Create messy dataset from Bob’s shop  #H
df = pd.DataFrame({  #I
    'purchase_date': ['12/31/2023', '2023-01-01', '01-15-2023'],  #J
    'sku': ['abc123', 'XYZ789', '123ABC'],  #K
    'product_description': [
        'red winter jacket - insulated and waterproof', 
        'bindings - lightweight and durable',
        'short snowboard - beginner friendly'
    ],  #L
    'first_name': ['Ava', 'Leo', 'Riley'],  #M
    'last_name': ['Smith', 'Nguyen', 'Patel'],  #N
    'product_name': ['winter jacket', 'bindings', 'short snowboard']  #O
})

# Format the dataset for the prompt  #P
records = df.to_dict(orient="records")  #Q

# Compose prompt to request all cleaning instructions in one shot  #R
prompt = (
    "You are a data cleaning assistant. Given a dataset, return the following lists with values that match the row order exactly:\n"
    "- A list of normalized purchase_date values in YYYY-MM-DD format.\n"
    "- A list of SKUs that match the format: 3 uppercase letters followed by 3 digits. If the SKU is invalid, return null.\n"
    "- A list of product_description values truncated to 20 characters.\n"
    "- A list of full_names by combining first_name and last_name.\n"
    "- A list of standardized product categories mapped from product_name. Use one of: outerwear, gear, boards.\n"
    "Each list must contain exactly one value per row, and values must be in the same order as the input records."
)


# Call OpenAI API with structured response  #S
completion = client.chat.completions.parse(
    model=MODEL_MAIN,
    messages=[
        {"role": "system", "content": prompt},  #T
        {"role": "user", "content": str(records)}  #U
    ],
    response_format=StandardizationInstructions  #V
)

# Parse structured output  #W
cleaned = completion.choices[0].message.parsed  #X

# Apply cleaned values to the original DataFrame  #Y
df['purchase_date'] = cleaned.normalized_dates
df['sku'] = cleaned.cleaned_skus
df['product_description'] = cleaned.truncated_descriptions
df['full_name'] = cleaned.full_names
df['product_category'] = cleaned.mapped_categories

# Show the cleaned DataFrame  #Z
print(df)  #AA
