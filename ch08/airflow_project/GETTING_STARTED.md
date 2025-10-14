# Getting Started with Airflow News Pipeline

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
cd airflow_project
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

**You should see a dashboard with `news_articles_pipeline`**

**Run it with default settings (Tesla articles):**
1. Find `news_articles_pipeline` in the list
2. Toggle the switch to **ON** (if it's paused)
3. Click the **▶️ play button** on the right
4. Select "Trigger DAG"
5. Watch it run! (takes 2-5 minutes)

**Want to search for a different company?** See the next section!

---

## Step 6: Run with Custom Parameters

**In your terminal:**

```bash
# First, get your container name
docker ps | grep airflow
# You'll see something like: airflow_project_airflow_1

# Then trigger with custom parameters
docker exec -it airflow_project_airflow_1 airflow dags trigger news_articles_pipeline \
  --conf '{"query": "Apple", "from_date": "2025-10-01", "to_date": "2025-10-08"}'
```

**Try different companies:**
- Tesla
- Apple
- Microsoft
- Amazon
- Google
- Any company or topic!

---

## Step 7: Check Your Data

**In your terminal:**
```bash
psql -h localhost -U news_user -d news_db
```

**Run these queries:**
```sql
-- How many articles?
SELECT COUNT(*) FROM news_articles;

-- Show me the latest 10
SELECT source, title, sentiment, topic
FROM news_articles
ORDER BY created_at DESC
LIMIT 10;

-- Exit when done
\q
```

**Congratulations! You've run your first AI-powered data pipeline!** 🎉

---

## What Just Happened?

The pipeline:
1. ✅ Fetched news articles from NewsAPI
2. ✅ Used AI to extract structured data
3. ✅ Analyzed sentiment (positive/negative)
4. ✅ Categorized by topic and region
5. ✅ Stored everything in your database

All automatically orchestrated by Airflow!

---

## Common Issues & Quick Fixes

### "Can't connect to PostgreSQL"

**Try this in your `.env`:**
```bash
PGHOST=host.docker.internal
```

Then restart:
```bash
docker compose restart
```

### "Invalid API key"

- Check your `.env` file has no spaces around `=`
- Make sure you copied the full key
- Restart after fixing: `docker compose restart`

### "DAG not showing up"

- Wait 30 seconds and refresh your browser
- Airflow scans for new DAGs every 30 seconds

### "Container not running"

```bash
docker ps | grep airflow
# If nothing shows up, start it:
./quickstart.sh
```

---

## Next Steps

1. ✅ You've run your first pipeline!
2. 🔄 Try different companies
3. 🔄 Try different date ranges
4. 🔄 Explore your data in PostgreSQL
5. 📖 Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for advanced features

---

## Useful Commands

```bash
# Stop Airflow
docker compose down

# Start Airflow
./quickstart.sh

# View logs
docker compose logs -f

# Check if it's running
docker ps | grep airflow
```

---

## Need More Help?

📖 **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Comprehensive guide with:
- Detailed troubleshooting
- Advanced usage
- Performance tips
- API cost optimization

---

**Happy data engineering! 🚀**

*Questions? Check SETUP_GUIDE.md or review the Airflow logs with `docker compose logs -f`*

