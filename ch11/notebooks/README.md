# Chapter 11 Notebooks

Technical resources for Chapter 11: *Identifying Opportunities for AI-Generated Data*

## Files

- **11_guide.ipynb** - Complete code listings from Chapter 11 (Listings 11.1-11.9)
- **11_lab.ipynb** - Lab exercises with solutions from sections 11.10-11.11
- **sample.env** - Template for API keys (copy to `.env` and fill in)

## Setup

### 1. Install Dependencies

```bash
pip install requests beautifulsoup4 pandas openai pydantic tiktoken python-dotenv
```

### 2. Configure API Keys

```bash
cp sample.env .env
# Edit .env with your API keys:
# - SERPAPI_KEY from https://serpapi.com
# - OPENAI_API_KEY from https://platform.openai.com
```

### 3. Run Notebooks

```bash
jupyter notebook 11_guide.ipynb
```

## Listings Covered

### 11_guide.ipynb

| Section | Listing | Topic |
|---------|---------|-------|
| 11.4.1 | 11.1 | SerpAPI product URL search |
| 11.4.2 | 11.2 | LLM URL ranking |
| 11.5.1 | 11.3 | Aggressive HTML cleaning (BeautifulSoup) |
| 11.5.2 | 11.4 | AI content triage |
| 11.6.1 | 11.5 | Pydantic extraction schema |
| 11.6.2 | 11.6 | AI product extraction |
| 11.6.3 | 11.7 | Manual vs AI comparison |
| 11.7.1 | 11.8 | Multi-site batch extraction |
| 11.8 | 11.9 | Token/cost estimation |

### 11_lab.ipynb

6 lab exercises covering:
1. Product selection (10 products, 3+ brands)
2. HTML fetching and cleaning
3. AI extraction
4. Results evaluation (success rate, field coverage)
5. Cost estimation (tokens, projections)
6. Manual vs AI comparison

## Cost Estimates (Real APIs)

| Stage | Model | Cost per Product |
|-------|-------|------------------|
| URL Ranking | gpt-4o-mini | ~$0.0003 |
| Content Triage | gpt-4o-mini | ~$0.0007 |
| Product Extraction | gpt-4o | ~$0.013 |
| **Total** | | **~$0.014** |

**450 products:** ~$6.30 (OpenAI) + ~$0.90 (SerpAPI) = **$7.20 total**

## Notes

- All code is production-ready
- Notebooks match ch10 formatting style
- Real API calls (no mocks)
- Execution requires valid API keys
- See `sample.env` for setup instructions

## Support

For questions, see Chapter 11 of *Data Engineering with AI* or contact the author.
