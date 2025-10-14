import pandas as pd
import openai
import re

# Define a function to handle missing values dynamically using OpenAI's API
def handle_missing_values(df, column, method="average"):  #A
    def impute_value(value, index, previous_value=None):
        if pd.notnull(value):  #B
            return value
        
        if method == "average":
            prompt = f"The current column is '{column}'. Fill the missing value at index {index} with the column's average. Here is the column data: {df[column].dropna().tolist()}. Strictly return only the imputed value as a number."  #C
        elif method == "static":
            prompt = f"The current column is '{column}'. Replace the missing value at index {index} with a static value of 25. Strictly return only the imputed value as a number."  #D
        elif method == "increment":
            prompt = f"The current column is '{column}'. Increment the previous value ({previous_value}) by 5% to replace the missing value at index {index}. Strictly return only the imputed value as a number."  #E
        else:
            raise ValueError("Invalid method specified.")
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        raw_response = response.choices[0].message.content.strip()  #F
        transformed_value = re.search(r"[-+]?\d*\.?\d+", raw_response)  #G
        if transformed_value:
            return float(transformed_value.group())  #H
        else:
            raise ValueError(f"Could not extract a valid numerical value from the response: {raw_response}")
    
    previous_value = None
    for idx, value in enumerate(df[column]):  #I
        df.at[idx, column] = impute_value(value, idx, previous_value)
        previous_value = df.at[idx, column]  #J

    return df  #K
