import pandas as pd
import openai

# Define a function to normalize numerical values using OpenAI's API
def normalize_numerical_values(df, column, task_description):
    def normalize_value(value):
        prompt = (
            f"Convert the following value from the column '{column}': {value}. "
            f"{task_description} Only return the numerical result, without any explanation or additional text."
        )
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content.strip()

    df[column] = df[column].apply(normalize_value)
    return df

# Example 1: Normalizing ZIP codes
df_zip = pd.DataFrame({'zip_code': [1001, 40004, 502]})
df_zip = normalize_numerical_values(df_zip, 'zip_code', "Format the ZIP code to always be 5 digits long by padding with zeros.")
print("Normalized ZIP Codes:\n", df_zip)
