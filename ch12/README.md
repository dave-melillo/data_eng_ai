# Chapter 12: AI-powered Web Scraping Data Pipelines in Action

This chapter takes the building blocks from Chapters 10 and 11 and assembles
them into a single, production-style enrichment pipeline. Each pipeline stage
becomes a small, single-responsibility **agent** (a Python function with a
typed contract), and the agents are chained together by an orchestrator that
tracks state, retries transient failures, logs progress, and routes uncertain
results to a human review queue.

## Learning Objectives
- Turn loose snippets into reusable, single-responsibility agents
- Design a Pydantic data contract for safe hand-offs between stages
- Chain agents into one orchestrated pipeline
- Add production concerns: retries/backoff, logging, status tracking
- Route low-confidence and invalid records to a human review queue
- Run the full RuckZone enrichment pipeline end to end and validate results

## The four agents
| Agent | File | Stage | LLM? |
|-------|------|-------|------|
| `discover_url`        | `listings/12_3.py` | URL discovery (Stage 2)       | yes (gpt-4o-mini) |
| `fetch_and_clean`     | `listings/12_4.py` | fetch + clean (Stage 3)       | no |
| `extract_product`     | `listings/12_5.py` | AI extraction (Stage 5)       | yes (gpt-4o) |
| `validate_and_map`    | `listings/12_6.py` | normalize + validate (Stage 6)| no |

The orchestrator (`listings/12_7.py`) chains them; `12_8.py` runs a batch and
`12_9.py` works the review queue and saves the trusted catalog.

## Contents
```
ch12/
├── README.md
├── requirements.txt
├── sample.env
├── data/
│   └── ruckzone_products.csv      # the batch used in the chapter + lab
├── listings/                       # one file per book listing
│   ├── 12_1.py  data contract (Pydantic models)
│   ├── 12_2.py  logging + retry decorator
│   ├── 12_3.py  Agent 1: discover_url
│   ├── 12_4.py  Agent 2: fetch_and_clean
│   ├── 12_5.py  Agent 3: extract_product
│   ├── 12_6.py  Agent 4: validate_and_map
│   ├── 12_7.py  orchestrator (run_one, run_pipeline)
│   ├── 12_8.py  run the full batch
│   └── 12_9.py  review queue + save catalog
├── notebooks/
│   ├── 12_guide.ipynb             # all listings, runnable in order
│   └── 12_lab.ipynb               # lab questions + starter
└── setup/
    └── chapter_12_setup.md
```

## Setup
1. Use Python 3.9+ and the repo's virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `sample.env` to `.env` and add your `OPENAI_API_KEY` and `SERPAPI_KEY`
   (see Appendix A and `setup/chapter_12_setup.md`).
4. Open `notebooks/12_guide.ipynb` and run the cells top to bottom.

> The pipeline makes live web requests and LLM calls, so exact results vary by
> run. If you do not have a SerpAPI key, see `setup/chapter_12_setup.md` for how
> to supply product URLs manually.

## Cost note
Per product, the pipeline makes one cheap ranking call (gpt-4o-mini) and one
extraction call (gpt-4o), roughly $0.015–0.02 per product. The five-product
chapter batch costs only a few cents. See Chapter 11, Section 11.8, for the
token-cost details.
