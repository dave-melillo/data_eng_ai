import openai
import pandas as pd

# Function to transform a DataFrame column using OpenAI's Chat Completions API
def chatgpt_transform_column(df, column, task_description, reference=None):  #A
    transformed_column = []  #B
    for value in df[column]:  #C
        # Build the prompt, including a reference list if provided
        if reference:
            prompt = f"{task_description}\nReference mapping: {reference}\nThe current value is: {value}. Only return the transformed value, nothing else."  #D
        else:
            prompt = f"{task_description} The current value is: {value}. Only return the transformed value, nothing else."  #E

        # Send the prompt to OpenAI's Chat Completions API
        response = openai.chat.completions.create(  #F
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        transformed_value = response.choices[0].message.content.strip()  #G
        transformed_column.append(transformed_value)  #H

    df[column] = transformed_column  #I
    return df  #J

#A Define function to transform a DataFrame column using OpenAI.
#B Initialize an empty list to store transformed values.
#C Loop through each value in the specified column of the DataFrame.
#D Build the prompt with a reference list if provided.
#E Build the prompt without reference if not needed.
#F Call OpenAI’s API with the prompt.
#G Extract the response content and strip whitespace.
#H Append the transformed value to the list.
#I Replace the column in the DataFrame with transformed values.
#J Return the modified DataFrame.
