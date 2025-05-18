import pandas as pd
import openai

# Define a function to clean text fields dynamically using OpenAI's API
def clean_text_fields(df, column, task_description):
    def clean_text(value):
        prompt = (
            f"The following text field: '{value}'. {task_description} "
            "Return only the cleaned text, nothing else."
        )

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content.strip()

    df[column] = df[column].apply(clean_text)
    return df
