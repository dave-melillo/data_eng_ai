import pandas as pd
import openai
import re

def clean_dataframe(df):
    prompt = f"Analyze this dataset and return True/False for duplicates: {df.to_dict(orient='records')}"  #A
    response = openai.ChatCompletion.create(model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )  #B

    duplicate_flags = re.findall(r'\b(True|False)\b', response['choices'][0]['message']['content'])  #C
    duplicate_flags = [flag == 'True' for flag in duplicate_flags]  #D

    if len(duplicate_flags) == len(df):  #E
        df = df[~pd.Series(duplicate_flags).values]  #F

    return df  #G

df = pd.DataFrame({
    'customer_id': [1, 2, 2, 3, 3],
    'preferred_store_location': ['NY', 'CA', 'CA', 'TX', None],
    'purchase_amount': [200, 300, 300, 400, 400],
    'optional_note': [None, None, None, None, None]
})

cleaned_df = clean_dataframe(df)  #H
print(cleaned_df)  #I
