"""
News Articles ETL Pipeline DAG

This DAG extracts news articles from NewsAPI, enriches them with AI-generated
summaries and sentiment analysis, and loads them into PostgreSQL.

Parameters (pass via trigger config):
- query: Company name to search for (default: "Tesla")
- from_date: Start date in YYYY-MM-DD format (default: yesterday)
- to_date: End date in YYYY-MM-DD format (default: today)
"""

from datetime import datetime, timedelta
import os
import logging
import json

from airflow.decorators import dag, task
from airflow.models import Variable

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


@dag(
    dag_id='news_articles_pipeline',
    default_args=default_args,
    description='Extract, transform, and load news articles with AI enrichment',
    schedule_interval=None,  # Manual trigger only
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['news', 'etl', 'ai'],
)
def news_articles_pipeline():
    
    @task()
    def extract_articles(**context):
        """
        Cell 1: Extract articles from NewsAPI
        
        Retrieves articles based on query and date range parameters.
        """
        import requests
        import pandas as pd
        from datetime import datetime, timedelta
        
        # Get parameters from trigger config or use defaults
        dag_run = context.get('dag_run')
        conf = dag_run.conf if dag_run else {}
        
        query = conf.get('query', 'Tesla')
        
        # Handle date parameters
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        from_date = conf.get('from_date', str(yesterday))
        to_date = conf.get('to_date', str(today))
        
        NEWS_API_KEY = os.getenv('NEWS_API_KEY')
        
        if not NEWS_API_KEY:
            raise ValueError("NEWS_API_KEY environment variable is not set")
        
        url = f'https://newsapi.org/v2/everything?q={query}&from={from_date}&to={to_date}&apiKey={NEWS_API_KEY}'
        
        logging.info(f"Fetching articles for query='{query}', from={from_date}, to={to_date}")
        
        response = requests.get(url)
        
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            logging.info(f"Successfully extracted {len(articles)} articles")
            
            # Return articles as list of dicts
            return {
                'articles': articles,
                'query': query,
                'from_date': from_date,
                'to_date': to_date,
                'count': len(articles)
            }
        else:
            logging.error(f"Failed to fetch articles. Status code: {response.status_code}")
            raise Exception(f"API request failed with status {response.status_code}")
    
    @task()
    def transform_articles(extract_result: dict):
        """
        Cell 2: Transform articles using OpenAI
        
        Extracts structured data and performs sentiment analysis.
        """
        import openai
        import pandas as pd
        from pydantic import BaseModel
        
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
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
        
        def perform_sentiment_analysis(text: str):
            """Analyze sentiment of text and return score from -1 to 1"""
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
        
        articles = extract_result['articles']
        results = []
        
        # Limit to prevent excessive API calls during testing (remove limit for production)
        max_articles = 5
        logging.info(f"Processing {min(len(articles), max_articles)} articles out of {len(articles)} total")
        
        for idx, article in enumerate(articles[:max_articles]):
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
                    item["sentiment"] = perform_sentiment_analysis(item["short_summary"])
                    results.append(item)
                    logging.info(f"Processed article {idx + 1}/{min(len(articles), max_articles)}")
            except Exception as e:
                logging.error(f"Error on article {idx}: {e}")
        
        logging.info(f"Successfully transformed {len(results)} articles")
        
        return {
            'extracted_articles': results,
            'metadata': extract_result
        }
    
    @task()
    def quality_check_and_categorize(transform_result: dict):
        """
        Cell 3: Quality check and categorize articles
        
        Adds timezone conversions, topic categorization, and region detection.
        """
        import openai
        import pandas as pd
        from pydantic import BaseModel
        
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        class QualityCategorization(BaseModel):
            short_date: str            # YYYY-MM-DD (no timezone)
            publish_est: str           # ISO-8601 datetime in America/New_York
            publish_pst: str           # ISO-8601 datetime in America/Los_Angeles
            publish_gmt: str           # ISO-8601 datetime in GMT/UTC (+00:00)
            topic: str                 # One of: Financial, Operations, Product/Technology, etc.
            region: str                # One of: North America, South America, Europe, etc.
        
        qc_system_prompt = f"""
You are a data quality and categorization agent. For each input article, return a single object matching this schema:
{QualityCategorization.schema_json(indent=2)}

Instructions:
- short_date: Derive from the input publish_date by dropping time and timezone, format as YYYY-MM-DD.
- publish_est / publish_pst / publish_gmt: Convert the input publish_date to the specified timezone and return ISO-8601 (include timezone offset).
- topic: Choose the best label from [Financial, Operations, Product/Technology, Regulatory/Legal, Market/Competition, Executive/Personnel, Strategy/M&A, Customers/Partnerships, Supply Chain/Manufacturing, ESG/Sustainability, Risk/Incidents, Marketing/PR].
- region: Infer using language cues, source, and content (country/city mentions). Map to one of: [North America, South America, Europe, Africa, Middle East, Asia, Oceania].
- Return strictly valid JSON with exactly these keys and no extra text.
        """.strip()
        
        extracted_articles = transform_result['extracted_articles']
        qc_results = []
        
        for idx, article in enumerate(extracted_articles):
            article_input = {
                "source": article.get("source", ""),
                "title": article.get("title", ""),
                "short_summary": article.get("short_summary", ""),
                "publish_date": article.get("publish_date", "")
            }
            try:
                completion = openai.beta.chat.completions.parse(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": qc_system_prompt},
                        {"role": "user", "content": f"{article_input}"}
                    ],
                    response_format=QualityCategorization
                )
                parsed = completion.choices[0].message.parsed
                if parsed:
                    qc_data = parsed.dict()
                    # Merge original article data with QC data
                    enriched_article = {**article, **qc_data}
                    qc_results.append(enriched_article)
                    logging.info(f"Enriched article {idx + 1}/{len(extracted_articles)}")
            except Exception as e:
                logging.error(f"QC error on article {idx}: {e}")
        
        logging.info(f"Successfully enriched {len(qc_results)} articles")
        
        return {
            'enriched_articles': qc_results,
            'metadata': transform_result['metadata']
        }
    
    @task()
    def load_to_postgres(enrichment_result: dict):
        """
        Cell 4: Load enriched articles to PostgreSQL
        
        Generates DDL if needed and inserts articles into the database.
        """
        import psycopg
        import openai
        from pydantic import BaseModel
        
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        class TableDDL(BaseModel):
            ddl: str
        
        # Define expected schema
        sample_fields = {
            "source": "text",
            "title": "text",
            "short_summary": "text",
            "publish_date": "timestamptz",
            "sentiment": "numeric",
            "short_date": "date",
            "publish_est": "timestamptz",
            "publish_pst": "timestamptz",
            "publish_gmt": "timestamptz",
            "topic": "text",
            "region": "text"
        }
        
        # Generate DDL using AI
        ddl_prompt = f"""
You are a SQL DDL assistant. Return only a single valid PostgreSQL CREATE TABLE statement for table name news_articles.
Use these columns and suggested types. Adjust types conservatively if needed, add NOT NULL only if obviously safe.
Columns:
{json.dumps(sample_fields, indent=2)}

Rules:
- Include a surrogate primary key id BIGSERIAL PRIMARY KEY.
- Add created_at TIMESTAMPTZ DEFAULT NOW().
- Use snake_case column names exactly as provided.
- Return strictly the SQL, no comments or extra text.
        """.strip()
        
        completion = openai.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": ddl_prompt},
                {"role": "user", "content": "Generate the DDL now."}
            ],
            response_format=TableDDL
        )
        TABLE_DDL = completion.choices[0].message.parsed.ddl
        logging.info(f"Generated DDL:\n{TABLE_DDL}")
        
        # Connect to PostgreSQL
        conn = psycopg.connect(
            host=os.getenv("PGHOST", "localhost"),
            port=os.getenv("PGPORT", "5432"),
            dbname=os.getenv("PGDATABASE", "news_db"),
            user=os.getenv("PGUSER", "news_user"),
            password=os.getenv("PGPASSWORD", "")
        )
        
        # Create table if not exists
        with conn.cursor() as cur:
            try:
                cur.execute(TABLE_DDL)
                logging.info("Table created successfully")
            except Exception as e:
                msg = str(e).lower()
                if "already exists" in msg:
                    logging.info("Table already exists, continuing...")
                else:
                    raise
        conn.commit()
        
        # Prepare insert
        cols = [
            "source", "title", "short_summary", "publish_date", "sentiment",
            "short_date", "publish_est", "publish_pst", "publish_gmt", "topic", "region"
        ]
        
        placeholders = ",".join(["%s"] * len(cols))
        insert_sql = f"INSERT INTO news_articles ({','.join(cols)}) VALUES ({placeholders})"
        
        # Convert articles to tuples
        enriched_articles = enrichment_result['enriched_articles']
        rows = []
        for article in enriched_articles:
            row = tuple(article.get(c) for c in cols)
            rows.append(row)
        
        # Batch insert
        with conn.cursor() as cur:
            if rows:
                cur.executemany(insert_sql, rows)
                logging.info(f"Inserted {len(rows)} rows into news_articles")
            else:
                logging.warning("No rows to insert")
        conn.commit()
        conn.close()
        
        return {
            'rows_inserted': len(rows),
            'metadata': enrichment_result['metadata']
        }
    
    @task()
    def verify_load(load_result: dict):
        """
        Cell 5: Verify data was loaded successfully
        
        Queries the database to confirm articles were inserted.
        """
        import psycopg
        import pandas as pd
        
        conn = psycopg.connect(
            host=os.getenv("PGHOST", "localhost"),
            port=os.getenv("PGPORT", "5432"),
            dbname=os.getenv("PGDATABASE", "news_db"),
            user=os.getenv("PGUSER", "news_user"),
            password=os.getenv("PGPASSWORD", "")
        )
        
        # Count total rows
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM news_articles;")
            total_rows = cur.fetchone()[0]
        
        logging.info(f"Total rows in news_articles: {total_rows}")
        
        # Get last 5 rows
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, source, title, publish_date, topic, region, sentiment, created_at
                FROM news_articles
                ORDER BY id DESC
                LIMIT 5;
            """)
            rows = cur.fetchall()
            cols = [c[0] for c in cur.description]
        
        conn.close()
        
        # Create DataFrame for logging
        df = pd.DataFrame(rows, columns=cols)
        logging.info(f"Latest 5 articles:\n{df.to_string()}")
        
        return {
            'total_rows': total_rows,
            'rows_inserted': load_result['rows_inserted'],
            'verification': 'success',
            'metadata': load_result['metadata']
        }
    
    # Define task dependencies
    extract_result = extract_articles()
    transform_result = transform_articles(extract_result)
    enrichment_result = quality_check_and_categorize(transform_result)
    load_result = load_to_postgres(enrichment_result)
    verify_result = verify_load(load_result)
    
    # Return final result
    return verify_result


# Instantiate the DAG
dag_instance = news_articles_pipeline()

