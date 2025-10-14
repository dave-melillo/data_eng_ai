import os
import logging
import openai
import pandas as pd
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class ExtractedArticle(BaseModel):
    source: str
    title: str
    short_summary: str
    publish_date: str

system_prompt = f"""
You are a data extraction agent. For each input article JSON, return a single object matching this schema:
{ExtractedArticle.schema_json(indent=2)}

Use the raw JSON to guide extraction with natural language hints:
- source: use article['source']['name'] when present.
- title: use article['title'].
- short_summary: 1–2 sentences summarizing the article in plain English.
- publish_date: use article['publishedAt'] (ISO-8601 timestamp).

Return exactly one object that matches the schema.
""".strip()

# Sentiment agent (adapted from news_api_tsla_full_pipeline)
def perform_sentiment_analysis(text: str):
    prompt = (
        "Analyze the sentiment of the following text and return a numerical sentiment "
        "score from -1 (very negative) to 1 (very positive). Return only the number: "
        f"{text}"
    )
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.3
        )
        sentiment_str = response.choices[0].message.content.strip()
        return float(sentiment_str)
    except Exception as e:
        logging.error(f"Error performing sentiment analysis: {e}")
        return None

results = []
input_articles = articles  # from prior cell

# Limit for quick iteration; adjust/remove as needed
for idx, article in enumerate(input_articles[:5]):
    try:
        completion = openai.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{article}"}
            ],
            response_format=ExtractedArticle
        )
        parsed = completion.choices[0].message.parsed
        if parsed:
            item = parsed.dict()
            item["sentiment"] = perform_sentiment_analysis(item["short_summary"])  # agent call
            results.append(item)
    except Exception as e:
        print(f"Error on article {idx}: {e}")

extracted_df = pd.DataFrame(results)
extracted_df
