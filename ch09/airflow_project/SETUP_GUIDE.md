# Chapter 9 Airflow Pipeline - Complete Setup Guide

This guide will help you set up and run the Chapter 9 data pipeline with Apache Airflow.

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

Extracts data → Transforms with AI → Loads to PostgreSQL

**Pipeline Tasks:**
1. **Extract** - Fetch data from source
2. **Transform** - AI-powered transformation
3. **Enrich** - Add analysis and metadata
4. **Load** - Insert into PostgreSQL
5. **Verify** - Confirm successful load

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

You need a PostgreSQL database to store the processed data.

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
- Supabase (free tier available)

**Note your connection details:**
- Host (e.g., `localhost` or cloud hostname)
- Port (default: `5432`)
- Database name: `news_db`
- Username: `news_user`
- Password: (your password)

### Database Schema

The pipeline automatically creates necessary tables on first run. No manual setup needed!

---

## Airflow Quick Start

### Step 1: Configure Environment

```bash
# Navigate to the project directory
cd ch09/airflow_project

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
3. You should see the Airflow dashboard with your DAG(s)

---

## Running the Pipeline

### Method 1: Via Web UI (Simple Trigger)

**For default parameters:**

1. Go to http://localhost:8080
2. Find your DAG in the list
3. Toggle it **ON** (if it shows as paused)
4. Click the **▶️ Play button** on the right
5. Select **"Trigger DAG"**
6. Watch the pipeline run!

### Method 2: Via CLI with Custom Parameters

```bash
# Get your container ID or name
docker ps | grep airflow

# Trigger with custom parameters
docker exec -it <container_id_or_name> airflow dags trigger your_dag_name \
  --conf '{"param1": "value1", "param2": "value2"}'
```

### Monitoring the Pipeline

**In the Web UI:**
1. Click on the DAG name to open detail view
2. Click on a run to see the Graph view
3. Watch tasks progress: gray → yellow (running) → green (success)
4. Click any task → "Log" button to see detailed logs

**Expected run time:** 2-10 minutes (depending on data volume and complexity)

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
-- List all tables
\dt

-- Count records
SELECT COUNT(*) FROM your_table;

-- View recent data
SELECT * FROM your_table
ORDER BY created_at DESC
LIMIT 10;

-- Exit
\q
```

---

## Troubleshooting

### Docker Issues

**Problem:** "Docker daemon not running"
```bash
# Fix: Start Docker Desktop application
# Wait for it to fully initialize (green icon)
docker ps  # Verify Docker is running
```

**Problem:** Port 8080 already in use
```bash
# Find what's using port 8080
lsof -i :8080

# Kill the process or change port in docker-compose.yaml
# ports: - "8081:8080"  # Use different external port
```

### PostgreSQL Connection Issues

**Problem:** "Connection refused" or "Could not connect"

**Fix 1: Change PGHOST**
```bash
# Edit .env file
nano .env

# Change from:
PGHOST=localhost

# To:
PGHOST=host.docker.internal

# Restart Airflow
docker compose restart
```

**Fix 2: Verify PostgreSQL is running**
```bash
# macOS:
brew services list | grep postgresql

# Linux:
sudo systemctl status postgresql

# Test connection from host:
psql -h localhost -U news_user -d news_db
```

**Fix 3: Check firewall/network**
- Ensure PostgreSQL accepts connections on port 5432
- Check `pg_hba.conf` for authentication rules

### API Key Issues

**Problem:** "Invalid API key" or "Unauthorized"

**Fix:**
```bash
# Verify .env file has correct keys
cat .env

# Check for extra spaces or newlines
# Keys should look like:
NEWS_API_KEY=abc123def456
OPENAI_API_KEY=sk-proj-abc123...

# Restart after fixing
docker compose restart
```

### DAG Not Appearing

**Problem:** DAG doesn't show in UI

**Fixes:**
1. Wait 30-60 seconds and refresh browser
2. Check DAG file for syntax errors:
   ```bash
   docker compose logs | grep -i error
   ```
3. Verify DAG file is in `dags/` directory
4. Check file has `.py` extension

### Task Failures

**Problem:** Task fails with error

**Debug steps:**
1. Click on the failed task in UI
2. Click "Log" button to see error details
3. Common issues:
   - Missing environment variables
   - API rate limits
   - Database connection timeout
   - Invalid data format

**View detailed logs:**
```bash
docker compose logs -f
```

### Container Issues

**Problem:** Container won't start or keeps restarting

**Fix:**
```bash
# Stop everything
docker compose down

# Remove volumes (WARNING: deletes Airflow data)
docker compose down -v

# Check for port conflicts
lsof -i :8080

# Start fresh
./quickstart.sh
```

---

## Advanced Usage

### Stopping and Restarting

```bash
# Stop Airflow (preserves data)
docker compose down

# Start again
./quickstart.sh

# OR just restart
docker compose restart
```

### Viewing Logs

```bash
# All logs
docker compose logs -f

# Last 100 lines
docker compose logs --tail=100

# Specific service
docker compose logs airflow
```

### Accessing the Container

```bash
# Get shell access
docker exec -it $(docker ps -q -f name=airflow) bash

# Inside container, you can:
airflow dags list           # List all DAGs
airflow dags trigger my_dag # Trigger a DAG
airflow tasks list my_dag   # List tasks in DAG
pip list                    # View installed packages
```

### Manual DAG Testing

```bash
# Test a specific task
docker exec -it $(docker ps -q -f name=airflow) \
  airflow tasks test my_dag task_name 2025-11-10

# Validate DAG syntax
docker exec -it $(docker ps -q -f name=airflow) \
  python /opt/airflow/dags/my_dag.py
```

### Custom Python Packages

**Add to docker-compose.yaml:**
```yaml
command: >
  bash -c "
    pip install --quiet your-package-name &&
    airflow db migrate &&
    airflow users create ... &&
    airflow standalone
  "
```

Then restart:
```bash
docker compose down
docker compose up -d
```

### Performance Tuning

**For faster startup:**
- Allocate more RAM to Docker (8GB recommended)
- Use SSD storage
- Close other memory-intensive applications

**For faster pipeline execution:**
- Batch operations when possible
- Use connection pooling for databases
- Implement caching for API responses
- Parallelize independent tasks

### Backup and Restore

**Backup your data:**
```bash
# Backup PostgreSQL database
pg_dump -h localhost -U news_user news_db > backup.sql

# Backup Airflow metadata (optional)
docker exec $(docker ps -q -f name=airflow) \
  sqlite3 /opt/airflow/airflow.db ".backup '/opt/airflow/backup.db'"
```

**Restore:**
```bash
# Restore PostgreSQL
psql -h localhost -U news_user -d news_db < backup.sql
```

### Cost Optimization

**OpenAI API:**
- Process smaller batches during development
- Use `gpt-4o-mini` for testing (cheaper)
- Cache results when possible
- Set usage limits in OpenAI dashboard

**NewsAPI:**
- Free tier: 100 requests/day
- Plan your queries to stay within limits
- Cache article data

---

## Common Commands Reference

```bash
# Start Airflow
./quickstart.sh

# Stop Airflow
docker compose down

# Restart
docker compose restart

# View logs
docker compose logs -f

# Check status
docker ps | grep airflow

# Access shell
docker exec -it $(docker ps -q -f name=airflow) bash

# Trigger DAG
docker exec -it $(docker ps -q -f name=airflow) \
  airflow dags trigger dag_name

# List DAGs
docker exec -it $(docker ps -q -f name=airflow) \
  airflow dags list

# Clean up (removes all data)
docker compose down -v
```

---

## Getting Help

### If You Encounter Issues

1. Check this troubleshooting guide first
2. Review error messages carefully
3. Check logs: `docker compose logs -f`
4. Verify all prerequisites are met
5. Try stopping and restarting: `docker compose down && ./quickstart.sh`

### Resources

- **Airflow Documentation**: https://airflow.apache.org/docs/
- **Docker Documentation**: https://docs.docker.com/
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **OpenAI API Docs**: https://platform.openai.com/docs

---

## Summary

You now have a complete Airflow pipeline setup! The key steps are:

1. ✅ Configure `.env` with your credentials
2. ✅ Run `./quickstart.sh`
3. ✅ Access http://localhost:8080
4. ✅ Trigger your DAG
5. ✅ Monitor execution and verify results

**Happy data engineering!** 🚀

