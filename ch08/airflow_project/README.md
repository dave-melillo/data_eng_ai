# News Articles ETL Pipeline with Apache Airflow

Automated pipeline that extracts news articles, enriches them with AI analysis, and loads them into PostgreSQL.

## Quick Overview

```
NewsAPI → OpenAI (Extract + Sentiment + Categorize) → PostgreSQL
```

**Pipeline Tasks:**
1. Extract articles from NewsAPI
2. Transform with OpenAI (extraction + sentiment)
3. Enrich with AI categorization (topic, region, timezones)
4. Load enriched data to PostgreSQL
5. Verify successful load

---

## Quick Start (3 Steps)

### 1. Prerequisites

- Docker Desktop (running)
- PostgreSQL database
- NewsAPI key (https://newsapi.org/)
- OpenAI API key (https://platform.openai.com/api-keys)

### 2. Configure

```bash
cp env.template .env
# Edit .env with your API keys and database credentials
```

### 3. Start

```bash
./quickstart.sh
```

Then open http://localhost:8080 (login: `airflow` / `airflow`)

**First run:** 2-3 minutes  
**Subsequent runs:** 30-60 seconds

---

## Trigger the Pipeline

### Simple (Default Parameters)

In the Airflow UI, click the ▶️ play button next to `news_articles_pipeline`

### With Custom Parameters

```bash
# Get your container name
docker ps | grep airflow

# Trigger with custom query and dates
docker exec -it <container_name> airflow dags trigger news_articles_pipeline \
  --conf '{"query": "Apple", "from_date": "2025-10-01", "to_date": "2025-10-08"}'
```

**Examples:**
- Tesla: `{"query": "Tesla", "from_date": "2025-10-05", "to_date": "2025-10-08"}`
- Apple: `{"query": "Apple", "from_date": "2025-10-01", "to_date": "2025-10-08"}`
- Microsoft: `{"query": "Microsoft", "from_date": "2025-09-15", "to_date": "2025-09-30"}`

---

## Documentation

📖 **New to Airflow?** Start here: **[GETTING_STARTED.md](GETTING_STARTED.md)**  
   - Absolute beginner's guide
   - Step-by-step instructions
   - Quick troubleshooting

📖 **Complete Reference:** **[SETUP_GUIDE.md](SETUP_GUIDE.md)**  
   - PostgreSQL setup instructions
   - Detailed troubleshooting
   - Advanced usage examples
   - Performance tips
   - API cost optimization

---

## Common Commands

```bash
# Start Airflow
./quickstart.sh

# Stop Airflow
docker compose down

# View logs
docker compose logs -f

# Restart
docker compose restart

# Check status
docker ps | grep airflow
```

---

## Project Structure

```
airflow_project/
├── dags/
│   └── news_pipeline_dag.py        # The ETL pipeline
├── docker-compose.yaml              # Airflow configuration
├── env.template                     # Environment variables template
├── .env                            # Your credentials (create this!)
├── quickstart.sh                    # Quick start script
├── SETUP_GUIDE.md                   # Complete documentation
└── README.md                        # This file
```

---

## Tech Stack

- **Airflow 2.7.0** - Workflow orchestration
- **NewsAPI** - Article extraction
- **OpenAI GPT-4** - AI analysis & enrichment
- **PostgreSQL** - Data storage
- **Docker** - Containerization

---

## What Gets Created

The pipeline automatically creates a `news_articles` table with:

- Article metadata (source, title, summary)
- AI-generated sentiment scores (-1 to 1)
- Topic categorization (Financial, Product, etc.)
- Regional classification (North America, Europe, etc.)
- Multi-timezone timestamps (EST, PST, GMT)

**Check your data:**
```sql
SELECT COUNT(*) FROM news_articles;

SELECT source, title, topic, sentiment
FROM news_articles
ORDER BY created_at DESC
LIMIT 10;
```

---

## Need Help?

1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) - Comprehensive troubleshooting
2. View logs: `docker compose logs -f`
3. Verify setup:
   - Docker is running: `docker ps`
   - PostgreSQL is accessible: `psql -h localhost -U news_user -d news_db`
   - Environment is configured: `cat .env`

---

**For complete setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)**
