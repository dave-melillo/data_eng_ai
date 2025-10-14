import os
import json
import logging
import pandas as pd
import openai
from pydantic import BaseModel

# Ensure psycopg is available
import sys, subprocess
try:
    import psycopg
except Exception:
    subprocess.run([sys.executable, "-m", "pip", "install", "psycopg[binary]>=3.1"], check=False)
    import psycopg

openai.api_key = os.getenv("OPENAI_API_KEY")

# Pydantic for DDL contract
class TableDDL(BaseModel):
    ddl: str  # CREATE TABLE ... statement only

# Model-friendly schema of enriched_df
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

# Compose prompt to generate DDL
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

# Ask AI for DDL
completion = openai.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": ddl_prompt},
        {"role": "user", "content": "Generate the DDL now."}
    ],
    response_format=TableDDL
)
TABLE_DDL = completion.choices[0].message.parsed.ddl
print(TABLE_DDL)

# Connect to Postgres
conn = psycopg.connect(
    host=os.getenv("PGHOST", "localhost"),
    port=os.getenv("PGPORT", "5432"),
    dbname=os.getenv("PGDATABASE", "news_db"),
    user=os.getenv("PGUSER", "news_user"),
    password=os.getenv("PGPASSWORD", "")
)

# Create table if not exists (idempotent):
with conn.cursor() as cur:
    try:
        cur.execute(TABLE_DDL)
    except Exception as e:
        # If table already exists, ignore
        msg = str(e).lower()
        if "already exists" not in msg:
            raise
conn.commit()

# Prepare insert (upsert optional)
cols = [
    "source", "title", "short_summary", "publish_date", "sentiment",
    "short_date", "publish_est", "publish_pst", "publish_gmt", "topic", "region"
]

placeholders = ",".join(["%s"] * len(cols))
insert_sql = f"INSERT INTO news_articles ({','.join(cols)}) VALUES ({placeholders})"

# Convert dataframe rows to tuples
rows = []
for _, r in enriched_df.iterrows():
    rows.append(tuple(r.get(c) for c in cols))

# Batch insert
with conn.cursor() as cur:
    if rows:
        cur.executemany(insert_sql, rows)
        print(f"Inserted {len(rows)} rows into news_articles")
    else:
        print("No rows to insert")
conn.commit()

conn.close()

