import pandas as pd
import openai

# Define a function to validate and categorize data using OpenAI's API
def categorize_items(df, column):
    def categorize_item(description):
        prompt = (  
            f"Given the following item description: '{description}', map it to one of these categories: "
            "'Records', 'CDs', 'Tapes', or 'Memorabilia'. If it does not fit, return 'Uncategorized'. "
            "Provide only the category name as your response."
        )
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content.strip()

    df['category'] = df[column].apply(categorize_item)
    return df

# Create a sample DataFrame with item descriptions
df = pd.DataFrame({'item_description': [
    'Led Zeppelin Vinyl', 
    'The Beatles CD', 
    'Pink Floyd Tour Poster', 
    'Elvis Cassette Tape', 
    'Rolling Stones T-Shirt'
]})

# Categorize items using OpenAI's API
df = categorize_items(df, 'item_description')

# Output the categorized DataFrame
print(df)
