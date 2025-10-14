# Chapter 8 Quick Start Guide

Get up and running with the multi-agent news pipeline in 15 minutes!

## What You'll Build

A news intelligence pipeline that:
- Extracts articles from NewsAPI
- Uses AI agents to analyze sentiment
- Categorizes by topic and region
- Stores enriched data in PostgreSQL

---

## Step-by-Step Setup

### ⏱️ Step 1: Check Prerequisites (2 min)

**You need:**
- Python 3.8 or higher
- Internet connection
- A text editor

**Check your Python version:**
```bash
python --version
# Should show Python 3.8.x or higher
```

---

### 📦 Step 2: Install Dependencies (3 min)

```bash
# Navigate to ch08 directory
cd ch08/

# Install required packages
pip install -r requirements.txt

# This installs: pandas, openai, psycopg, pydantic, requests, python-dotenv
```

**Verify installation:**
```bash
pip list | grep -E "(pandas|openai|psycopg)"
```

---

### 🔑 Step 3: Get Your API Keys (5 min)

#### NewsAPI Key (FREE)

1. Go to: https://newsapi.org/
2. Click "Get API Key"
3. Sign up with your email
4. Copy your API key (looks like: `a1b2c3d4e5f6...`)

**Free tier includes:**
- 100 requests per day
- Last 30 days of articles
- Perfect for learning!

#### OpenAI API Key (PAID - ~$5 for all exercises)

1. Go to: https://platform.openai.com/
2. Sign in or create account
3. Go to "API keys" section
4. Click "Create new secret key"
5. Name it "Chapter 8 Pipeline"
6. Copy the key immediately (starts with `sk-proj-...`)

**⚠️ Important:**
- Requires payment method on file
- Set usage limit to $10/month to avoid surprises
- Estimated cost for chapter: $5-10 total

---

### 🗄️ Step 4: Set Up PostgreSQL Database (5 min)

#### Option A: Use Supabase (Easiest - No Installation)

1. Go to: https://supabase.com/
2. Sign up (free)
3. Create new project
   - Name: `news-pipeline`
   - Database password: (create a strong password - save it!)
   - Region: Choose closest to you
4. Wait 2 minutes for project creation
5. Go to Settings → Database → Connection string
6. Copy the connection details:
   - Host: `db.xxxxx.supabase.co`
   - Port: `5432`
   - Database: `postgres`
   - User: `postgres`
   - Password: (your project password)

✅ **Advantage:** No installation, works from anywhere, free forever

#### Option B: Install PostgreSQL Locally

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Windows:**
- Download from: https://www.postgresql.org/download/windows/
- Run installer, remember your password
- Use default port 5432

**Create Database:**
```bash
# Connect to PostgreSQL
psql postgres

# Inside PostgreSQL prompt, run:
CREATE DATABASE news_db;
CREATE USER news_user WITH PASSWORD 'secure_password_123';
GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;
\c news_db
GRANT ALL ON SCHEMA public TO news_user;
\q
```

**Test connection:**
```bash
psql -h localhost -U news_user -d news_db
# Enter your password
# You should see: news_db=>
\q
```

📚 **Need help?** See `setup/postgres_setup.md` for detailed instructions

---

### ⚙️ Step 5: Configure Environment Variables (2 min)

```bash
# From ch08 directory, copy the template
cp setup/sample.env notebooks/.env

# Edit the file with your actual credentials
nano notebooks/.env
# OR
code notebooks/.env  # if using VS Code
```

**Fill in your actual values:**

```bash
# Replace these with your real credentials:
NEWS_API_KEY=paste_your_newsapi_key_here
OPENAI_API_KEY=sk-proj-paste_your_openai_key_here

# For Supabase users:
PGHOST=db.xxxxxxxxxxxxx.supabase.co
PGPORT=5432
PGDATABASE=postgres
PGUSER=postgres
PGPASSWORD=your_supabase_password

# For Local PostgreSQL users:
PGHOST=localhost
PGPORT=5432
PGDATABASE=news_db
PGUSER=news_user
PGPASSWORD=secure_password_123
```

**💡 Tip:** Never commit `.env` files to git! They contain secrets.

---

### ✅ Step 6: Verify Everything Works (3 min)

```bash
# From ch08 directory, run:
python verify_setup.py
```

**You should see:**
```
✅ Python version: 3.x.x
✅ All dependencies installed
✅ Environment variables set
✅ NewsAPI connected
✅ OpenAI API connected
✅ PostgreSQL connected
✅ Pipeline test passed

🎉 ALL CHECKS PASSED!
You're ready to start Chapter 8!
```

**If anything fails:**
- Read the error messages carefully
- Check the corresponding section above
- See `setup/postgres_setup.md` for database help

---

## Running Your First Pipeline

### Option 1: Interactive Notebook (Recommended)

```bash
# Start Jupyter
cd notebooks/
jupyter lab

# OR
jupyter notebook

# Open 8_guide.ipynb and run the cells!
```

**What the notebook does:**
1. Extracts Tesla news from NewsAPI
2. Uses AI to extract structured data + sentiment
3. Categorizes by topic and region
4. Generates PostgreSQL schema
5. Loads data to database
6. Queries results

### Option 2: Run Code Listings

```bash
# From ch08 directory

# Extract articles from NewsAPI
python listing/8_1.py

# Transform with AI agents
python listing/8_2.py

# Enrich with categorization
python listing/8_3.py

# Generate schema and load to database
python listing/8_4_8_5.py
```

### Option 3: Disney Lab Exercise

```bash
# Start Jupyter and open the lab notebook
jupyter lab notebooks/8_lab.ipynb

# This builds a Disney news pipeline with business line categorization!
# Categories: Parks, Movies, Streaming/Disney+, Merchandise, ESPN/Sports, etc.
```

---

## What to Expect

### Data Volume
- **NewsAPI** returns 0-100 articles per query (free tier limit)
- **Guide examples** process 5 articles for quick iteration
- **Full runs** can process all returned articles

### Processing Time
- **Extract**: ~1-2 seconds per API call
- **Transform**: ~2-3 seconds per article (AI processing)
- **Load**: <1 second for batch insert
- **Total for 5 articles**: ~30 seconds

### API Costs
- **NewsAPI**: FREE (100 requests/day)
- **OpenAI**: ~$0.10-0.20 per 5 articles processed
- **Complete guide**: ~$1-2
- **Complete lab**: ~$2-3
- **Total for chapter**: ~$5-10

💡 **Tip:** Set OpenAI usage limit to $10/month in your dashboard

---

## Understanding the Pipeline

### The Multi-Agent Architecture

```
┌─────────────────────────────────────────────────┐
│  NewsAPI  →  Extraction Agent  →  DataFrame     │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  Sentiment Agent  →  Adds sentiment scores      │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  Categorization Agent  →  Topics + Regions      │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  Schema Agent  →  Generates CREATE TABLE DDL    │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  Load Agent  →  Inserts into PostgreSQL         │
└─────────────────────────────────────────────────┘
```

### Why Multiple Agents?

Each agent has a **single responsibility**:
- **Easier to debug** - Know exactly where errors occur
- **Easier to test** - Validate each agent independently
- **Easier to modify** - Change one agent without affecting others
- **More maintainable** - Clear separation of concerns

---

## Viewing Your Results

### In PostgreSQL

```bash
# Connect to database
psql -h localhost -U news_user -d news_db

# Inside psql:
```

```sql
-- Count total articles
SELECT COUNT(*) FROM news_articles;

-- View latest 5 articles
SELECT source, title, sentiment, topic
FROM news_articles
ORDER BY created_at DESC
LIMIT 5;

-- Average sentiment by topic
SELECT topic, 
       COUNT(*) as count,
       ROUND(AVG(sentiment)::numeric, 2) as avg_sentiment
FROM news_articles
GROUP BY topic
ORDER BY count DESC;

-- Exit
\q
```

### In Python/Jupyter

```python
import pandas as pd
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

# Connect
conn = psycopg.connect(
    host=os.getenv('PGHOST'),
    port=os.getenv('PGPORT'),
    dbname=os.getenv('PGDATABASE'),
    user=os.getenv('PGUSER'),
    password=os.getenv('PGPASSWORD')
)

# Query to DataFrame
df = pd.read_sql("SELECT * FROM news_articles ORDER BY created_at DESC LIMIT 10", conn)
display(df)

conn.close()
```

---

## Troubleshooting Quick Reference

### ❌ "NewsAPI key not working"
**Fix:** Verify key at https://newsapi.org/account - Copy and paste carefully into `.env`

### ❌ "OpenAI authentication error"
**Fix:** Check you have payment method on file at https://platform.openai.com/account/billing

### ❌ "PostgreSQL connection refused"
**Fix:** 
```bash
# Verify service running
brew services list | grep postgresql  # macOS
sudo systemctl status postgresql      # Linux

# Start if stopped
brew services start postgresql@15     # macOS
```

### ❌ "Database 'news_db' does not exist"
**Fix:**
```bash
psql postgres -c "CREATE DATABASE news_db;"
```

### ❌ "Permission denied for schema public"
**Fix:**
```bash
psql -U postgres -d news_db -c "GRANT ALL ON SCHEMA public TO news_user;"
```

### ❌ "Module not found: openai/psycopg/pydantic"
**Fix:**
```bash
pip install -r requirements.txt
```

---

## Next Steps

### 1. Run the Guide Notebook

```bash
jupyter lab notebooks/8_guide.ipynb
```

Work through the Tesla news pipeline to understand each agent.

### 2. Complete the Lab

```bash
jupyter lab notebooks/8_lab.ipynb
```

Build a Disney analytics pipeline with business line categorization!

### 3. Try Custom Queries

Modify the extraction to search for different companies:
- Apple
- Microsoft  
- Amazon
- Your favorite company!

### 4. Explore Airflow (Optional)

For production orchestration:
```bash
cd airflow_project/
./quickstart.sh
```

See `airflow_project/GETTING_STARTED.md` for complete Airflow setup.

---

## Learning Path

**Beginner Path:**
1. ✅ Complete this quick start
2. 📓 Work through `8_guide.ipynb` notebook
3. 🧪 Complete `8_lab.ipynb` exercise
4. 🚀 Experiment with different companies/queries

**Advanced Path:**
1. ✅ Complete beginner path
2. 📝 Modify agent prompts to change categorization
3. 🔧 Add new agents (duplicate detection, competitor tracking)
4. ⚙️ Set up Airflow orchestration
5. 🏗️ Deploy to production with monitoring

---

## Cost Tracking

### Monitor Your Usage

**OpenAI:**
- Dashboard: https://platform.openai.com/usage
- Set email alerts when you reach 50% of limit
- Typical usage: $0.10-0.20 per 5 articles

**NewsAPI:**
- Dashboard: https://newsapi.org/account
- Free tier: 100 requests/day
- Each pipeline run = 1 request

### Cost Optimization Tips

1. **Start small** - Process 5 articles first, then scale up
2. **Set limits** - Configure max spend in OpenAI dashboard
3. **Cache results** - Save API responses to avoid reprocessing
4. **Use batches** - Process articles in groups of 10-20

---

## Getting Help

### Resources

- **PostgreSQL Issues**: See `setup/postgres_setup.md`
- **Chapter README**: `../README.md` for comprehensive docs
- **Airflow Setup**: `airflow_project/GETTING_STARTED.md`
- **Manning Book Forums**: For community support

### Quick Help Commands

```bash
# Check Python version
python --version

# Check installed packages
pip list | grep -E "(pandas|openai|psycopg)"

# Test database connection
psql -h localhost -U news_user -d news_db -c "SELECT 1;"

# Verify environment variables
python -c "from dotenv import load_dotenv; load_dotenv('notebooks/.env'); import os; print('API keys loaded' if os.getenv('OPENAI_API_KEY') else 'No API key')"

# Run full verification
python verify_setup.py
```

---

## Success Indicators

You're ready when:
- ✅ `python verify_setup.py` shows all checks passed
- ✅ You can connect to PostgreSQL: `psql -h localhost -U news_user -d news_db`
- ✅ NewsAPI test returns articles
- ✅ OpenAI test completes successfully

---

## Common First-Time Issues

### "I don't have PostgreSQL installed"

**Easiest solution:** Use Supabase (free, no installation)
1. https://supabase.com/ → Sign up
2. Create project → Copy connection details
3. Use in your `.env` file

### "My .env file isn't being loaded"

**Check location:**
```bash
# For notebooks, put it here:
ls notebooks/.env  # Should exist

# If not:
cp setup/sample.env notebooks/.env
```

### "OpenAI says I need to add payment"

**Solution:**
1. Go to https://platform.openai.com/account/billing
2. Add a credit card
3. Set a monthly usage limit (e.g., $10)
4. Wait a few minutes for activation

### "I'm getting rate limit errors"

**For NewsAPI:**
- Free tier = 100 requests/day
- Wait 24 hours or upgrade

**For OpenAI:**
- Free tier has low limits
- Add payment method for higher limits
- Or reduce batch size (process fewer articles)

---

## What's Next?

### Learning Path

**Week 1: Understand the Pipeline**
- Day 1-2: Run `8_guide.ipynb` completely
- Day 3-4: Complete `8_lab.ipynb` Disney exercise
- Day 5: Experiment with different companies

**Week 2: Customize and Extend**
- Add new agent types (competitor tracking, entity extraction)
- Modify categorization logic
- Add new database columns
- Build custom dashboards

**Week 3: Production Deployment**
- Set up Airflow orchestration
- Implement monitoring and alerting
- Schedule daily runs
- Optimize costs and performance

---

## Quick Command Reference

```bash
# Setup
pip install -r requirements.txt
cp setup/sample.env notebooks/.env
python verify_setup.py

# Run notebooks
jupyter lab notebooks/8_guide.ipynb

# Run listings
python listing/8_1.py  # Extract
python listing/8_2.py  # Transform
python listing/8_3.py  # Enrich
python listing/8_4_8_5.py  # Load

# Database
psql -h localhost -U news_user -d news_db
SELECT COUNT(*) FROM news_articles;

# Airflow (optional)
cd airflow_project/
./quickstart.sh
open http://localhost:8080
```

---

## Ready to Start?

Run the verification script:
```bash
python verify_setup.py
```

If all checks pass:
```bash
jupyter lab notebooks/8_guide.ipynb
```

**Have fun building your multi-agent news pipeline! 🚀**

