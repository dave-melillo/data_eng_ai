import logging
import openai
import pandas as pd
from pydantic import BaseModel

class QualityCategorization(BaseModel):
    short_date: str            # YYYY-MM-DD (no timezone)
    publish_est: str           # ISO-8601 datetime in America/New_York
    publish_pst: str           # ISO-8601 datetime in America/Los_Angeles
    publish_gmt: str           # ISO-8601 datetime in GMT/UTC (+00:00)
    topic: str                 # One of: Financial, Operations, Product/Technology, Regulatory/Legal, Market/Competition, Executive/Personnel, Strategy/M&A, Customers/Partnerships, Supply Chain/Manufacturing, ESG/Sustainability, Risk/Incidents, Marketing/PR
    region: str                # One of: North America, South America, Europe, Africa, Middle East, Asia, Oceania

qc_system_prompt = f"""
You are a data quality and categorization agent. For each input article, return a single object matching this schema:
{QualityCategorization.schema_json(indent=2)}

Instructions:
- short_date: Derive from the input publish_date by dropping time and timezone, format as YYYY-MM-DD.
- publish_est / publish_pst / publish_gmt: Convert the input publish_date to the specified timezone and return ISO-8601 (include timezone offset). Use the original timestamp as ground truth. Do not guess.
- topic: Choose the best label from [Financial, Operations, Product/Technology, Regulatory/Legal, Market/Competition, Executive/Personnel, Strategy/M&A, Customers/Partnerships, Supply Chain/Manufacturing, ESG/Sustainability, Risk/Incidents, Marketing/PR]. If none is perfect, pick the closest and be consistent.
- region: Infer using language cues, source, and content (country/city mentions). Map to one of:
  [North America, South America, Europe, Africa, Middle East, Asia, Oceania]. Always use exactly these labels.
- Return strictly valid JSON with exactly these keys and no extra text.
""".strip()

qc_results = []

for idx, row in extracted_df.iterrows():
    article_input = {
        "source": row.get("source", ""),
        "title": row.get("title", ""),
        "short_summary": row.get("short_summary", ""),
        "publish_date": row.get("publish_date", "")
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
            qc_results.append(parsed.dict())
        else:
            qc_results.append({
                "short_date": "",
                "publish_est": "",
                "publish_pst": "",
                "publish_gmt": "",
                "topic": "",
                "region": ""
            })
    except Exception as e:
        logging.error(f"QC error on row {idx}: {e}")
        qc_results.append({
            "short_date": "",
            "publish_est": "",
            "publish_pst": "",
            "publish_gmt": "",
            "topic": "",
            "region": ""
        })

qc_df = pd.DataFrame(qc_results)
enriched_df = pd.concat([extracted_df.reset_index(drop=True), qc_df], axis=1)
enriched_df
