# Airflow News Pipeline - Complete Setup Guide

This guide will help you set up and run the News Articles ETL pipeline with Apache Airflow.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [PostgreSQL Setup](#postgresql-setup)
3. [Airflow Quick Start](#airflow-quick-start)
4. [Running the Pipeline](#running-the-pipeline)
5. [Verifying Your Data](#verifying-your-data)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Usage](#advanced-usage)

---

## What This Pipeline Does

Extracts news articles → Enriches with AI → Loads to PostgreSQL

**5 Tasks:**
1. **Extract** - Fetch articles from NewsAPI
2. **Transform** - AI extraction + sentiment analysis (OpenAI)
3. **Enrich** - Categorize by topic/region, add timezones
4. **Load** - Insert into PostgreSQL
5. **Verify** - Confirm successful load

**Parameters:**
- `query` - Company to search for (default: "Tesla")
- `from_date` - Start date YYYY-MM-DD (default: yesterday)
- `to_date` - End date YYYY-MM-DD (default: today)

---

## Prerequisites

Before starting, ensure you have:

1. **Docker Desktop** installed and running
   - Download: https://www.docker.com/products/docker-desktop
   - Verify: `docker --version`
   - Allocate at least 4GB RAM to Docker

2. **API Keys**:
   - **NewsAPI**: Get free key at https://newsapi.org/
   - **OpenAI**: Get key at https://platform.openai.com/api-keys

3. **PostgreSQL Database** (see next section)

---

## PostgreSQL Setup

You need a PostgreSQL database to store the enriched news articles.

### Option 1: Local PostgreSQL (Recommended for Development)

**Install PostgreSQL:**
- **macOS**: `brew install postgresql@15` then `brew services start postgresql@15`
- **Windows**: Download from https://www.postgresql.org/download/windows/
- **Linux**: `sudo apt-get install postgresql-15`

**Create Database and User:**

```bash
# Connect to PostgreSQL
psql postgres

# In the PostgreSQL prompt, run:
CREATE DATABASE news_db;
CREATE USER news_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;
\q
```

**Verify connection:**
```bash
psql -h localhost -U news_user -d news_db
# Enter your password when prompted
```

### Option 2: Cloud PostgreSQL

Use any cloud provider:
- AWS RDS
- Google Cloud SQL
- Azure Database for PostgreSQL
- ElephantSQL (free tier available)

**Note your connection details:**
- Host (e.g., `localhost` or cloud hostname)
- Port (default: `5432`)
- Database name: `news_db`
- Username: `news_user`
- Password: (your password)

### Database Schema

The pipeline automatically creates the `news_articles` table on first run. No manual setup needed!

The table includes:
- Article metadata (source, title, summary)
- AI analysis (sentiment score)
- Categorization (topic, region)
- Timestamps (multiple timezones)

---

## Airflow Quick Start

### Step 1: Configure Environment

```bash
# Navigate to the project directory
cd airflow_project

# Create .env file from template
cp env.template .env
```

**Edit `.env` with your credentials:**

```bash
# Open in your text editor
nano .env  # or: vim .env, code .env, etc.
```

**Required configuration:**
```bash
# API Keys
NEWS_API_KEY=your_newsapi_key_here
OPENAI_API_KEY=sk-proj-your_openai_key_here

# PostgreSQL Connection
PGHOST=localhost                    # Use 'host.docker.internal' if Docker can't access localhost
PGPORT=5432
PGDATABASE=news_db
PGUSER=news_user
PGPASSWORD=your_db_password_here
```

**Important Notes:**
- **For local PostgreSQL**: Try `PGHOST=localhost` first. If that doesn't work, use `PGHOST=host.docker.internal`
- **For cloud PostgreSQL**: Use the hostname provided by your cloud provider
- Never commit your `.env` file (it's in `.gitignore`)

### Step 2: Start Airflow

```bash
./quickstart.sh
```

**What this does:**
- Checks Docker is running
- Creates necessary directories
- Starts Airflow container
- Installs Python dependencies (openai, psycopg, pandas, pydantic)
- Waits for Airflow to be ready

**First run:** 2-3 minutes (downloads image, installs packages)  
**Subsequent runs:** 30-60 seconds

**You'll see:**
```
========================================
  ✅ Airflow is Running!
========================================

🌐 http://localhost:8080
   Username: airflow
   Password: airflow
```

### Step 3: Access Web UI

1. Open your browser to: **http://localhost:8080**
2. Login with:
   - Username: `airflow`
   - Password: `airflow`
3. You should see the Airflow dashboard with your `news_articles_pipeline` DAG

---

## Running the Pipeline

### Method 1: Via Web UI (Simple Trigger)

**For default parameters (Tesla, yesterday-today):**

1. Go to http://localhost:8080
2. Find `news_articles_pipeline` in the DAG list
3. Toggle it **ON** (if it shows as paused)
4. Click the **▶️ Play button** on the right
5. Select **"Trigger DAG"**
6. Watch the pipeline run!

### Method 2: Via CLI with Custom Parameters (Recommended)

**This is the easiest way to customize the query and dates:**

```bash
# Get your container ID or name
docker ps | grep airflow

# Trigger with custom parameters
docker exec -it <container_id_or_name> airflow dags trigger news_articles_pipeline \
  --conf '{"query": "Apple", "from_date": "2025-10-01", "to_date": "2025-10-08"}'
```

**Example with actual container name:**
```bash
docker exec -it airflow_project_airflow_1 airflow dags trigger news_articles_pipeline \
  --conf '{"query": "Microsoft", "from_date": "2025-10-01", "to_date": "2025-10-08"}'
```

**Parameter examples:**

```bash
# Tesla (tech company)
docker exec -it airflow_project_airflow_1 airflow dags trigger news_articles_pipeline \
  --conf '{"query": "Tesla", "from_date": "2025-10-05", "to_date": "2025-10-08"}'

# Apple
docker exec -it airflow_project_airflow_1 airflow dags trigger news_articles_pipeline \
  --conf '{"query": "Apple", "from_date": "2025-10-01", "to_date": "2025-10-08"}'

# Amazon AWS (specific topic)
docker exec -it airflow_project_airflow_1 airflow dags trigger news_articles_pipeline \
  --conf '{"query": "Amazon AWS", "from_date": "2025-09-15", "to_date": "2025-09-30"}'
```

### Monitoring the Pipeline

**In the Web UI:**
1. Click on the DAG name to open detail view
2. Click on a run to see the Graph view
3. Watch tasks progress: gray → yellow (running) → green (success)
4. Click any task → "Log" button to see detailed logs

**Expected run time:** 2-5 minutes (depending on number of articles and API response times)

**Task sequence:**
1. ✅ `extract_articles` - Fetches from NewsAPI (~10 seconds)
2. ✅ `transform_articles` - AI processing (~30-60 seconds)
3. ✅ `quality_check_and_categorize` - More AI (~30-60 seconds)
4. ✅ `load_to_postgres` - Database insert (~5 seconds)
5. ✅ `verify_load` - Confirmation (~2 seconds)

---

## Verifying Your Data

After the pipeline runs successfully, check your database:

### Via Command Line

```bash
# Connect to your database
psql -h localhost -U news_user -d news_db

# Or if using cloud database:
psql -h your_cloud_host -U news_user -d news_db
```

### Useful Queries

```sql
-- Count total articles
SELECT COUNT(*) FROM news_articles;

-- View latest articles
SELECT id, source, title, topic, region, sentiment, created_at
FROM news_articles
ORDER BY created_at DESC
LIMIT 10;

-- Articles by topic
SELECT topic, COUNT(*) as count
FROM news_articles
GROUP BY topic
ORDER BY count DESC;

-- Articles by region
SELECT region, COUNT(*) as count
FROM news_articles
GROUP BY region
ORDER BY count DESC;

-- Average sentiment by source
SELECT source, AVG(sentiment) as avg_sentiment, COUNT(*) as articles
FROM news_articles
GROUP BY source
HAVING COUNT(*) > 2
ORDER BY avg_sentiment DESC;

-- Recent articles with full details
SELECT 
    source,
    title,
    short_summary,
    topic,
    region,
    sentiment,
    short_date
FROM news_articles
ORDER BY created_at DESC
LIMIT 5;
```

---

## Common Commands

### Airflow Management

```bash
# Start Airflow
./quickstart.sh

# Stop Airflow
docker compose down

# View live logs
docker compose logs -f

# Restart Airflow
docker compose restart

# Check container status
docker ps | grep airflow

# Check Airflow health
curl http://localhost:8080/health
```

### Triggering DAGs

```bash
# Get container name
docker ps | grep airflow

# Trigger with default params
docker exec -it <container_name> airflow dags trigger news_articles_pipeline

# Trigger with custom params
docker exec -it <container_name> airflow dags trigger news_articles_pipeline \
  --conf '{"query": "Tesla", "from_date": "2025-10-05", "to_date": "2025-10-08"}'

# List all DAGs
docker exec -it <container_name> airflow dags list

# Check DAG status
docker exec -it <container_name> airflow dags state news_articles_pipeline
```

### Debugging

```bash
# View specific task logs
docker exec -it <container_name> airflow tasks logs \
  news_articles_pipeline extract_articles <run_id>

# Check for errors
docker compose logs | grep ERROR

# Verify environment variables
docker exec -it <container_name> env | grep -E "NEWS_API|OPENAI_API|PG"

# Test Python imports
docker exec -it <container_name> python -c "import openai, psycopg, pandas; print('OK')"

# Validate DAG syntax
docker exec -it <container_name> python /opt/airflow/dags/news_pipeline_dag.py
```

---

## Troubleshooting

### Issue: DAG Not Showing Up

**Solution:**
- Wait 30 seconds (Airflow scans for DAGs every 30 seconds)
- Refresh the browser
- Check logs: `docker compose logs | grep news_pipeline`
- Verify DAG file has no syntax errors

### Issue: "ModuleNotFoundError" for openai, psycopg, etc.

**Solution:**
Dependencies are installed automatically on container startup. If you still see import errors:

```bash
# Restart to reinstall packages
docker compose restart

# Or manually install
docker exec -it <container_name> pip install openai psycopg pandas pydantic python-dotenv
```

### Issue: Can't Connect to PostgreSQL

**Symptoms:** Tasks fail with "could not connect to server" or "connection refused"

**Solutions:**

1. **Verify PostgreSQL is running:**
   ```bash
   # Test local connection
   psql -h localhost -U news_user -d news_db
   ```

2. **Try different host in `.env`:**
   ```bash
   # If localhost doesn't work, try:
   PGHOST=host.docker.internal
   
   # Then restart Airflow
   docker compose restart
   ```

3. **Check credentials:**
   - Verify username, password, database name
   - Make sure user has proper permissions

4. **Test from inside container:**
   ```bash
   docker exec -it <container_name> python << 'EOF'
   import psycopg
   import os
   conn = psycopg.connect(
       host=os.getenv('PGHOST'),
       port=os.getenv('PGPORT'),
       dbname=os.getenv('PGDATABASE'),
       user=os.getenv('PGUSER'),
       password=os.getenv('PGPASSWORD')
   )
   print("Connection successful!")
   conn.close()
   EOF
   ```

### Issue: API Key Errors

**Symptoms:** Tasks fail with "401 Unauthorized" or "Invalid API key"

**Solutions:**

1. **Verify keys are set:**
   ```bash
   docker exec -it <container_name> env | grep -E "NEWS_API_KEY|OPENAI_API_KEY"
   ```

2. **Check `.env` file format:**
   - No spaces around `=`
   - No quotes needed
   - Example: `NEWS_API_KEY=abc123xyz`

3. **Restart after changing `.env`:**
   ```bash
   docker compose down
   docker compose up -d
   ```

### Issue: Tasks Failing

**How to diagnose:**

1. **View task logs in UI:**
   - Click on failed task (red square)
   - Click "Log" button
   - Read the error message

2. **Common errors and fixes:**
   - `AttributeError: 'ExtractedArticle' has no attribute 'model_json_schema'` → Already fixed in DAG
   - `Rate limit exceeded` → Wait and retry, or reduce article count
   - `Timeout` → Increase timeout in DAG or check internet connection

### Issue: Container Keeps Restarting

**Solutions:**

```bash
# Check what's wrong
docker compose logs

# Common causes:
# 1. Insufficient memory - allocate 4GB+ to Docker
# 2. Port 8080 already in use - stop other services
# 3. Invalid .env file - check for syntax errors

# Fresh start
docker compose down -v  # Warning: removes all data!
docker compose up -d
```

### Issue: Airflow UI Not Loading

**Solutions:**

1. **Wait longer:** First startup takes 2-3 minutes
2. **Check container status:**
   ```bash
   docker ps | grep airflow
   ```
3. **Check health:**
   ```bash
   curl http://localhost:8080/health
   ```
4. **View logs:**
   ```bash
   docker compose logs -f
   ```

---

## Advanced Usage

### Increasing Article Processing Limit

By default, the pipeline processes 5 articles (to save API costs during testing).

**To process more articles:**

Edit `dags/news_pipeline_dag.py`:

```python
# Find this line (around line 158):
max_articles = 5

# Change to:
max_articles = 20  # or any number you want
```

Restart Airflow to apply changes:
```bash
docker compose restart
```

### Scheduling Automatic Runs

Currently, the DAG runs only when manually triggered. To schedule automatic runs:

Edit `dags/news_pipeline_dag.py`:

```python
@dag(
    dag_id='news_articles_pipeline',
    ...
    schedule_interval='0 9 * * *',  # Daily at 9 AM UTC
    ...
)
```

**Common schedules:**
- `'@daily'` - Once per day at midnight
- `'@hourly'` - Every hour
- `'0 9 * * *'` - Daily at 9 AM
- `'0 9 * * 1-5'` - Weekdays at 9 AM
- `'0 */6 * * *'` - Every 6 hours
- `None` - Manual only (current setting)

Learn more about cron syntax: https://crontab.guru/

### Reducing API Costs

The pipeline makes **3 OpenAI API calls per article**:
1. Extraction (1 call)
2. Sentiment analysis (1 call)
3. Categorization (1 call)

**Ways to reduce costs:**

1. **Limit articles processed** (already set to 5)
2. **Use cheaper model** - Edit DAG to use `gpt-3.5-turbo` instead of `gpt-4o`
3. **Process less frequently** - Don't schedule, run manually as needed
4. **Batch similar queries** - Process multiple date ranges for same company

### Custom Date Ranges

```bash
# Last 7 days
docker exec -it <container_name> airflow dags trigger news_articles_pipeline \
  --conf '{"query": "Tesla", "from_date": "2025-10-02", "to_date": "2025-10-09"}'

# Specific month
docker exec -it <container_name> airflow dags trigger news_articles_pipeline \
  --conf '{"query": "Apple", "from_date": "2025-09-01", "to_date": "2025-09-30"}'

# Single day
docker exec -it <container_name> airflow dags trigger news_articles_pipeline \
  --conf '{"query": "Microsoft", "from_date": "2025-10-08", "to_date": "2025-10-08"}'
```

### Multiple Companies

Run the pipeline multiple times with different queries:

```bash
for company in Tesla Apple Microsoft Amazon Google; do
    docker exec -it <container_name> airflow dags trigger news_articles_pipeline \
      --conf "{\"query\": \"$company\", \"from_date\": \"2025-10-01\", \"to_date\": \"2025-10-08\"}"
    sleep 5  # Wait between triggers
done
```

---

## Architecture

### What We're Using

- ✅ **Airflow 2.7.0** - Stable version that works reliably on macOS
- ✅ **SQLite** - For Airflow metadata (avoids Docker/PostgreSQL permission issues)
- ✅ **Sequential Executor** - Simple, reliable, perfect for development
- ✅ **Single Container** - Easy to manage and troubleshoot
- ✅ **Your PostgreSQL** - For news articles data (separate from Airflow)

### How It Works

```
┌─────────────────────────────────────┐
│   Docker Container (Airflow 2.7.0) │
│                                     │
│   ┌─────────────┐                  │
│   │  Webserver  │ :8080            │
│   └──────┬──────┘                  │
│          │                          │
│   ┌──────┴──────┐                  │
│   │  Scheduler  │                  │
│   └──────┬──────┘                  │
│          │                          │
│   ┌──────┴──────┐                  │
│   │SQLite (.db) │ (metadata)       │
│   └─────────────┘                  │
│                                     │
│   DAG: news_articles_pipeline      │
│   ├─ Extract (NewsAPI)             │
│   ├─ Transform (OpenAI)            │
│   ├─ Enrich (AI)                   │
│   ├─ Load → PostgreSQL             │
│   └─ Verify                         │
└─────────────────────────────────────┘
           │
           ↓
  ┌────────────────┐
  │  PostgreSQL    │ (your news_db)
  │  (local/cloud) │
  └────────────────┘
```

### Why This Setup?

**vs. Standard Airflow (CeleryExecutor + PostgreSQL + Redis):**

- ✅ **Simpler** - One container instead of 4-5
- ✅ **No macOS issues** - Avoids Docker/PostgreSQL threading problems
- ✅ **Easier to debug** - All logs in one place
- ✅ **Perfect for learning** - Focus on workflows, not infrastructure
- ✅ **Still production-capable** - Fine for moderate workloads

**Note:** Your news_db PostgreSQL is still used for storing articles. SQLite is only for Airflow's internal metadata.

---

## File Structure

```
airflow_project/
├── dags/
│   └── news_pipeline_dag.py        # The ETL pipeline (5 tasks)
├── docker-compose.yaml              # Airflow container config
├── .env                            # Your credentials (create from template)
├── env.template                     # Template with required vars
├── quickstart.sh                    # One-command startup script
├── requirements.txt                 # Python dependencies
├── trigger_config.example.json      # Example DAG parameters
├── README.md                        # Quick overview
├── SETUP_GUIDE.md                   # This comprehensive guide
├── .gitignore                       # Git ignore rules
│
├── airflow-data/                    # Auto-generated (SQLite DB, config)
├── logs/                            # Auto-generated (Airflow logs)
├── plugins/                         # Custom plugins (empty)
└── config/                          # Additional configs (empty)
```

**Note:** `airflow-data/` and `logs/` are created automatically on first run.

---

## Next Steps

1. ✅ Set up PostgreSQL database
2. ✅ Configure `.env` with your credentials
3. ✅ Start Airflow with `./quickstart.sh`
4. ✅ Trigger pipeline with default params (Tesla)
5. ✅ Check data in PostgreSQL
6. 🔄 Try different companies (Apple, Microsoft, Google)
7. 🔄 Experiment with date ranges
8. 🔄 Increase article processing limit
9. 🔄 Set up scheduled runs (optional)
10. 🔄 Customize the DAG for your needs

---

## Getting Help

**Check logs first:**
```bash
docker compose logs -f
```

**Common issues are covered in:**
- [Troubleshooting](#troubleshooting) section above
- [Common Commands](#common-commands) for quick reference

**Verification checklist:**
- [ ] Docker Desktop is running with 4GB+ RAM
- [ ] PostgreSQL is running and accessible
- [ ] `.env` file has all required variables
- [ ] API keys are valid
- [ ] Container is running: `docker ps | grep airflow`
- [ ] Health check passes: `curl http://localhost:8080/health`

**External resources:**
- Airflow documentation: https://airflow.apache.org/docs/
- NewsAPI docs: https://newsapi.org/docs
- OpenAI API docs: https://platform.openai.com/docs

---

**You're all set! 🚀 Happy data engineering!**
