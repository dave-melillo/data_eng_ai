# World Series Game 7 Analysis Pipeline

AI-powered pipeline that analyzes play-by-play baseball commentary and extracts structured data, player statistics, and excitement metrics.

## Quick Overview

```
Load CSV (729 plays)
    ↓
Extract Game Data (innings, scores, players, pitches) [AI]
    ↓
Map to Canonical IDs (clean names) [AI]
    ↓
Analyze Excitement & Key Moments [AI]
    ↓
Generate Summary Statistics
```

**What You Get:**
- Structured game data from unstructured text
- Player and pitch type canonical mappings
- Excitement ratings (1-10) for every play
- Key moment identification
- Pitcher and batter statistics

---

## Quick Start (3 Steps)

### 1. Prerequisites

- Docker Desktop (running)
- OpenAI API key (https://platform.openai.com/api-keys)

### 2. Configure

```bash
cp env.template .env
# Edit .env with your OpenAI API key
```

**Required:**
```bash
OPENAI_API_KEY=sk-your-key-here
```

### 3. Start & Run

```bash
./quickstart.sh
# Open http://localhost:8080 (login: airflow / airflow)
# Trigger DAG: world_series_analysis
```

**First run:** 2-3 minutes  
**Pipeline run:** 2 minutes (10 rows) or 20 minutes (all 729 rows)

---

## ⚙️ Configure Number of Rows (IMPORTANT!)

**For TESTING (10 rows):**
```python
# Edit dags/world_series_pipeline.py line 28:
NUM_ROWS = 10  # Fast testing (~2 min, ~$0.50)
```

**For FULL ANALYSIS (729 rows):**
```python
# Edit dags/world_series_pipeline.py line 28:
NUM_ROWS = 0  # Complete analysis (~20 min, ~$5-7)
```

**After changing NUM_ROWS:**
```bash
docker compose restart  # Restart to apply changes
```

---

## Trigger the Pipeline

### Via UI
1. Open http://localhost:8080
2. Find `world_series_analysis`
3. Click ▶️ → "Trigger DAG"
4. Watch it run!

---

## Documentation

📖 **Start Here:** **[QUICK_START.md](QUICK_START.md)** ⭐  
   - 5-minute setup guide
   - How to configure NUM_ROWS
   - Cost estimates

📖 **New to Airflow?** **[GETTING_STARTED.md](GETTING_STARTED.md)**  
   - Absolute beginner's guide
   - Step-by-step instructions

📖 **Troubleshooting:** **[SETUP_GUIDE.md](SETUP_GUIDE.md)**  
   - Detailed troubleshooting
   - Advanced usage

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
│   └── (your DAG files here)
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
- **NewsAPI** - Data extraction
- **OpenAI GPT-4** - AI analysis
- **PostgreSQL** - Data storage
- **Docker** - Containerization

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

