```
     ___       _          ___                _                      _
    |   \ __ _| |_ __ _  | __|_ _  __ _ _ _(_)_ _  ___ ___ _ _ _ _(_)_ _  __ _
    | |) / _` |  _/ _` | | _|| ' \/ _` | ' \| | ' \/ -_) -_| '_| | ' \/ _` |
    |___/\__,_|\__\__,_| |___|_||_\__, |_||_|_|_||_\___\___|_| |_|_||_\__, |
                                  |___/                                |___/
                         __      __)  __    __
                        (, |  | /  (/  () /(
                          | /| /     / / /
                          |/ |/   __/ (_/  _
                          /  |  (_/ /  / _(/
                                       /
```

# Data Engineering with AI

### Companion code repository for the [Manning](https://www.manning.com/) book by Dave Melillo

---

This repo contains all the notebooks, code listings, datasets, and setup guides for **Data Engineering with AI** — a hands-on book that teaches data engineers how to integrate LLMs and AI tools into real-world data pipelines.

## What You'll Build

Starting from basic prompt engineering and progressing to production Airflow pipelines with multi-agent architectures, each chapter includes executable Jupyter notebooks, lab exercises, and real datasets.

```
 ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
 │  Prompting   │───▶│   API       │───▶│  Pipelines  │───▶│  Production │
 │  SQL/Python  │    │  Integration│    │  & Agents   │    │  Workflows  │
 └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
   Chapters 2-4       Chapter 5         Chapters 6-8       Chapters 9-11
```

## Chapters

| Ch | Topic | What You'll Learn |
|----|-------|-------------------|
| **01** | Before You Begin | Environment setup — PostgreSQL, Jupyter, OpenAI API |
| **02** | AI/LLM Coding Companions | Benefits, limitations, and practical use cases with JSON and the Pagila dataset |
| **03** | Coding Companions & SQL | Zero-shot, few-shot, chain-of-thought prompting for SQL query generation |
| **04** | Coding Companions & Python | API integration, JSON flattening, regex with AI assistance |
| **05** | OpenAI API in Data Workflows | Embedding LLMs in code, NewsAPI integration, sentiment analysis pipelines |
| **06** | Data Quality & Validation | Data profiling, validation frameworks, error detection |
| **07** | Advanced Data Transformations | Entity resolution, hierarchical data, time series — traditional vs AI approaches |
| **08** | AI & the Data Lifecycle | Multi-agent architectures, extraction/transformation/enrichment agents, Airflow orchestration |
| **09** | Advanced Pipeline Orchestration | Production Airflow: complex dependencies, scheduling, monitoring, multi-environment deployment |
| **10** | The Web Scraping Challenge | HTTP requests, HTML parsing, understanding extraction limitations |
| **11** | AI-Generated Data Opportunities | URL discovery with SerpAPI, AI-powered content triage, product data extraction with LLMs |

## Tech Stack

```
 ╔══════════════════════════════════════════════════════════════════╗
 ║  Languages        Python 3.8+ · SQL (PostgreSQL)               ║
 ║  AI / LLM         OpenAI API (GPT-4o) · Pydantic · tiktoken   ║
 ║  Data              pandas · numpy · BeautifulSoup · rapidfuzz  ║
 ║  APIs              NewsAPI · SerpAPI · Open Brewery DB          ║
 ║  Infrastructure    Apache Airflow · Docker · PostgreSQL         ║
 ║  Notebooks         Jupyter Lab                                  ║
 ╚══════════════════════════════════════════════════════════════════╝
```

## Repo Structure

```
data_eng_ai/
├── ch01/ - ch11/            # One directory per chapter
│   ├── README.md            # Chapter overview & objectives
│   ├── notebooks/
│   │   ├── *_guide.ipynb    # Full chapter walkthrough
│   │   └── *_lab.ipynb      # Hands-on lab exercises
│   ├── listings/            # Individual code examples
│   ├── setup/               # Data files & setup scripts
│   ├── requirements.txt     # Chapter dependencies
│   └── sample.env           # API key template
│
└── setup/                   # Shared setup guides
    ├── postgres_setup.md
    ├── jupyter_setup.md
    ├── openai_setup.md
    └── ...
```

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/dave-melillo/data_eng_ai.git
cd data_eng_ai
```

### 2. Set up your environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 3. Follow the chapter setup guides

Each chapter has its own `README.md` and `requirements.txt`. Start with the shared guides in `setup/` for PostgreSQL, Jupyter, and API key configuration.

```bash
cd ch01
pip install -r requirements.txt
```

### 4. Launch Jupyter

```bash
jupyter lab
```

## Prerequisites

| Requirement | Chapters |
|-------------|----------|
| Python 3.8+ | All |
| PostgreSQL + pgAdmin | 1–5, 8–9 |
| OpenAI API key | 2–11 |
| Docker Desktop | 8–9 |
| NewsAPI key | 5, 8–9 |
| SerpAPI key | 11 |

## Datasets

- **Pagila** — PostgreSQL sample database (film rentals)
- **Open Brewery DB** — U.S. brewery data
- **NewsAPI** — Real news articles for analysis
- **RuckZone Products** — ~445 outdoor gear products for enrichment exercises
- Various JSON/CSV samples for transformation practice

---

<p align="center">
  <sub>Published by Manning Publications · Written by Dave Melillo</sub>
</p>
