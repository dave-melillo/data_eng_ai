# Chapter 11 Notebooks - Dependencies

## Overview
These notebooks demonstrate AI-assisted data extraction techniques from Chapter 11. To keep the notebooks executable without external API dependencies, certain API calls have been mocked with realistic placeholder data.

## Mocked Components

### API Keys
The following API calls are mocked in the notebooks:

1. **SerpAPI** (`search_product_urls`)
   - **Original purpose:** Search for product URLs via Google search API
   - **Mock behavior:** Returns 3 hardcoded candidate URLs with titles, snippets, and positions
   - **To use real API:** Set `SERPAPI_KEY` environment variable and replace mock with actual `requests.get()` call

2. **OpenAI API** (`rank_urls_with_ai`, `extract_product_with_ai`)
   - **Original purpose:** Use GPT models for URL ranking and product data extraction
   - **Mock behavior:** 
     - URL ranking: Simple heuristic (prefers official manufacturer sites)
     - Product extraction: Regex-based text parsing for price/weight
   - **To use real API:** 
     - Install: `pip install openai pydantic`
     - Set `OPENAI_API_KEY` environment variable
     - Replace mock classes with `from pydantic import BaseModel, Field`
     - Replace mock extraction with actual `openai.beta.chat.completions.parse()` calls

### HTML Fetching
- **Mock:** `11_lab.ipynb` uses pre-defined mock HTML snippets instead of live HTTP requests
- **Reason:** Avoids external dependencies and potential site blocking
- **To use real fetching:** Install `requests` and `beautifulsoup4`, replace mock text with actual `requests.get()` calls

## Required Packages (Real Implementation)

```bash
pip install requests beautifulsoup4 pandas openai pydantic tiktoken
```

### Optional (for SerpAPI)
```bash
# SerpAPI Python client (optional, requests works too)
pip install google-search-results
```

## Environment Variables (Real Implementation)

```bash
export SERPAPI_KEY="your_serpapi_key_here"
export OPENAI_API_KEY="your_openai_key_here"
```

## Running the Notebooks

### As-is (Mocked)
```bash
cd ch11/notebooks
jupyter notebook 11_guide.ipynb  # or 11_lab.ipynb
```

All cells will execute successfully with mocked data. No API keys required.

### With Real APIs
1. Install packages listed above
2. Set environment variables
3. Replace mock functions with real API calls (see inline comments in notebooks)
4. Run notebooks

## Cost Estimates (Real Implementation)

When using real OpenAI API calls:
- **URL Ranking** (gpt-4o-mini): ~$0.0003 per product
- **Content Triage** (gpt-4o-mini): ~$0.0007 per product
- **Product Extraction** (gpt-4o): ~$0.013 per product
- **Total per product:** ~$0.014
- **450 products:** ~$6.30

SerpAPI costs ~$0.002 per search (free tier: 100 searches/month).

## Notes

- The mock implementations produce realistic outputs that match the chapter examples
- All code patterns and structures are production-ready; only API calls are mocked
- Token counting uses a simplified estimator (1 token ≈ 4 characters) instead of tiktoken
- For production use, review OpenAI's [Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs)

## Support

For questions about the code or mocked components, see Chapter 11 of *Data Engineering with AI* or contact the author.
