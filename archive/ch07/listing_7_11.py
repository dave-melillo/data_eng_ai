import pandas as pd
import openai
import re

# Define a function to normalize time zones dynamically using OpenAI's API
def normalize_timezones(df, column):
    def normalize_timestamp(timestamp):
        prompt = (
            f"The following timestamp '{timestamp}' is recorded in its respective time zone. "
            "Convert it to UTC and strictly return the result in ISO-8601 format (e.g., 'YYYY-MM-DDTHH:MM:SSZ')."
        )
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        
        raw_response = response.choices[0].message.content.strip()
        iso8601_match = re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", raw_response)
        
        if iso8601_match:
            return iso8601_match.group()
        else:
            raise ValueError(f"Invalid UTC format returned by OpenAI's API: {raw_response}")

    df['utc_timestamp'] = df[column].apply(normalize_timestamp)
    return df

# Create a sample DataFrame with timestamps in different formats and time zones
df = pd.DataFrame({
    'timestamp': ['2024-03-01 12:00:00 EST', '2024-03-01 5:00 PM GMT', '2024-03-01T09:00:00+05:00']
})

# Normalize timestamps using OpenAI's API
df = normalize_timezones(df, 'timestamp')

# Output the standardized DataFrame
print(df)
