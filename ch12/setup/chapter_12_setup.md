# Chapter 12 Setup Guide

**Chapter:** AI-powered Web Scraping Data Pipelines in Action
**Builds on:** Chapters 10 and 11

This chapter assembles the Chapter 11 building blocks into one orchestrated
pipeline, so the setup is the same as Chapter 11 plus nothing new. If you ran
Chapter 11, you are ready.

## 1. Prerequisites
- Python 3.9 or newer (the data contract uses `typing` generics)
- The repo's virtual environment, activated
- An OpenAI API key (extraction + ranking agents)
- A SerpAPI key (URL discovery agent) — optional, see Section 4

Full environment setup (Python, venv, Jupyter, API keys) is covered in
**Appendix A, "Setting Up Your Environment."**

## 2. Install dependencies
```bash
cd ch12
pip install -r requirements.txt
```

## 3. Configure API keys
```bash
cp sample.env .env
# then edit .env and add:
#   OPENAI_API_KEY=...
#   SERPAPI_KEY=...
```
Load them in the notebook with:
```python
from dotenv import load_dotenv
load_dotenv()
```

## 4. Running without a SerpAPI key
The URL discovery agent (`discover_url`, Listing 12.3) uses SerpAPI. If you do
not have a key, you can bypass discovery and feed the pipeline URLs directly:

```python
# Minimal stand-in for discover_url when you already have URLs.
from listings... import URLRanking  # or paste the class from 12_3.py

KNOWN_URLS = {
    "GORUCK GR1 26L": "https://www.goruck.com/products/gr1",
    # add your own brand+product -> URL mappings here
}

def discover_url(search_key):
    url = KNOWN_URLS.get(search_key)
    if not url:
        return None
    return URLRanking(best_url=url, confidence="high",
                      reasoning="manually supplied")
```
Define this **before** `run_one` so the orchestrator picks it up. Everything
downstream (fetch, extract, validate) still runs normally and still uses your
OpenAI key.

## 5. Run order
Open `notebooks/12_guide.ipynb` and run cells top to bottom. The listings are
order-dependent: the data contract and shared helpers (12.1, 12.2) must run
before the agents (12.3–12.6), which must run before the orchestrator (12.7)
and the batch run (12.8, 12.9).

## 6. Verify
A successful run prints a per-product log, a results DataFrame with a `status`
column, and a non-zero count for at least one of `success` / `needs_review`.
Because the pipeline hits the live web, exact results vary between runs.

## Troubleshooting
- **`SERPAPI_KEY` is None** — you skipped `load_dotenv()` or `.env` is missing.
  Either set the key or use the manual-URL approach in Section 4.
- **Many records fail at `fetch`** — some sites block automated traffic or
  render product data with JavaScript that `requests` cannot execute. That is
  expected; those records are recorded as failed, not crashed.
- **`openai.OpenAIError` on every extract** — check your `OPENAI_API_KEY`,
  billing status, and that `openai>=1.0.0` is installed.
