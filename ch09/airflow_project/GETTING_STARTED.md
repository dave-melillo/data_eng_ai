# Getting Started with Chapter 9 Airflow Pipeline

**Quick start guide for absolute beginners**

---

## Before You Begin

You need:
- [ ] Docker Desktop installed and running
- [ ] A PostgreSQL database
- [ ] A NewsAPI key
- [ ] An OpenAI API key

**Don't have these?** See [SETUP_GUIDE.md](SETUP_GUIDE.md#prerequisites) for detailed setup instructions.

---

## Step 1: Get Your API Keys

### NewsAPI (Free)
1. Go to https://newsapi.org/
2. Click "Get API Key"
3. Sign up (it's free!)
4. Copy your API key

### OpenAI (Paid - but cheap for testing)
1. Go to https://platform.openai.com/api-keys
2. Sign up and add $5-10 credit
3. Click "Create new secret key"
4. Copy your API key (starts with `sk-proj-...`)

---

## Step 2: Set Up PostgreSQL

If you don't have PostgreSQL installed:

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Windows:** Download from https://www.postgresql.org/download/windows/

**Create the database:**
```bash
# Connect to PostgreSQL
psql postgres

# Create database and user (run these commands in psql)
CREATE DATABASE news_db;
CREATE USER news_user WITH PASSWORD 'choose_a_password';
GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;
\q
```

**Test it works:**
```bash
psql -h localhost -U news_user -d news_db
# Enter your password when prompted
# If you can connect, you're good! Type \q to exit
```

---

## Step 3: Configure the Pipeline

**Open your terminal and navigate to this directory:**
```bash
cd ch09/airflow_project
```

**Create your configuration file:**
```bash
cp env.template .env
```

**Edit `.env` with your information:**
```bash
nano .env  # or use any text editor
```

**Fill in your details:**
```bash
NEWS_API_KEY=paste_your_newsapi_key_here
OPENAI_API_KEY=sk-proj-paste_your_openai_key_here
PGHOST=localhost
PGPASSWORD=your_postgres_password_here
```

**Save the file!** (In nano: Ctrl+X, then Y, then Enter)

---

## Step 4: Start Airflow

```bash
./quickstart.sh
```

**Wait for this message:**
```
✅ Airflow is Running!
🌐 http://localhost:8080
   Username: airflow
   Password: airflow
```

**First time?** This takes 2-3 minutes. Grab a coffee! ☕

---

## Step 5: Run Your First Pipeline

**Open your browser:**
1. Go to http://localhost:8080
2. Login:
   - Username: `airflow`
   - Password: `airflow`

**You should see a dashboard with your DAG(s)**

**Run it with default settings:**
1. Find your DAG in the list
2. Toggle the switch to **ON** (if it's paused)
3. Click the **▶️ play button** on the right
4. Select "Trigger DAG"
5. Watch it run! (takes 2-5 minutes)

---

## Step 6: Run with Custom Parameters

**In your terminal:**

```bash
# First, get your container name
docker ps | grep airflow
# You'll see something like: airflow_project_airflow_1

# Then trigger with custom parameters
docker exec -it airflow_project_airflow_1 airflow dags trigger your_dag_name \
  --conf '{"param1": "value1", "param2": "value2"}'
```

---

## Step 7: Check Your Data

**In your terminal:**
```bash
psql -h localhost -U news_user -d news_db
```

**Run these queries:**
```sql
-- List all tables
\dt

-- Show data
SELECT * FROM your_table LIMIT 10;

-- Exit when done
\q
```

**Congratulations! You've run your first AI-powered data pipeline!** 🎉

---

## What Just Happened?

The pipeline:
1. ✅ Extracted data from source
2. ✅ Used AI to transform data
3. ✅ Enriched with analysis
4. ✅ Stored everything in your database

All automatically orchestrated by Airflow!

---

## Common Issues & Quick Fixes

### "Docker daemon not running"
**Fix:** Open Docker Desktop and wait for it to start

### "Can't connect to PostgreSQL"
**Fix:** Change `PGHOST=localhost` to `PGHOST=host.docker.internal` in `.env`
```bash
nano .env  # Change the line
docker compose restart  # Restart Airflow
```

### "DAG not showing up"
**Fix:** Wait 30 seconds and refresh the browser. DAGs take a moment to appear!

### "Invalid API key"
**Fix:** Double-check your `.env` file has the correct keys (no extra spaces!)
```bash
cat .env  # Verify your keys
```

---

## Useful Commands

```bash
# Stop Airflow
docker compose down

# Start again
./quickstart.sh

# View logs (helpful for debugging)
docker compose logs -f

# Restart without stopping
docker compose restart
```

---

## Next Steps

- Explore the Airflow UI at http://localhost:8080
- Check the DAG graph view (click on your DAG → Graph)
- View task logs (click on a task → Logs)
- Try running with different parameters
- Query your database to see the results

---

## Need More Help?

- **Complete setup guide:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Project overview:** [README.md](README.md)
- **Check logs:** `docker compose logs -f`

**Still stuck?** Make sure:
1. Docker Desktop is running
2. Your `.env` file has valid API keys
3. PostgreSQL is accessible
4. Port 8080 is not in use by another application

