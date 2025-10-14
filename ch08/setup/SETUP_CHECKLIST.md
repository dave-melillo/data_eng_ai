# Chapter 8 Setup Checklist

Use this checklist to ensure you have everything configured correctly before starting the chapter.

---

## ✅ Pre-Setup Checklist

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Can use command line/terminal
- [ ] Have a text editor (VS Code, nano, vim, etc.)
- [ ] Internet connection available

---

## ✅ Dependencies Installation

- [ ] Navigated to `ch08/` directory
- [ ] Created virtual environment (optional but recommended)
  ```bash
  python -m venv venv
  source venv/bin/activate  # macOS/Linux
  # OR venv\Scripts\activate  # Windows
  ```
- [ ] Installed all dependencies
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Verified installation
  ```bash
  pip list | grep -E "(pandas|openai|psycopg|pydantic)"
  ```

---

## ✅ NewsAPI Setup

- [ ] Created account at https://newsapi.org/
- [ ] Copied API key from dashboard
- [ ] Tested key works (returns articles)
- [ ] Noted free tier limits:
  - 100 requests/day
  - Articles from last 30 days only

**Your NewsAPI key:** `__________________________`

---

## ✅ OpenAI API Setup

- [ ] Created account at https://platform.openai.com/
- [ ] Added payment method in Billing section
- [ ] Generated new API key
- [ ] Saved key securely (starts with `sk-proj-...`)
- [ ] Set monthly usage limit ($10 recommended)
- [ ] Key format verified (starts with `sk-`)

**Your OpenAI key:** `sk-proj-__________________`

---

## ✅ PostgreSQL Database Setup

### Choose ONE option:

#### Option A: Supabase (Cloud - No Installation)
- [ ] Created account at https://supabase.com/
- [ ] Created new project
- [ ] Saved database password
- [ ] Copied connection details from Settings → Database
- [ ] Connection details noted:
  - Host: `db.________________.supabase.co`
  - Port: `5432`
  - Database: `postgres`
  - User: `postgres`
  - Password: `_______________`

#### Option B: Local PostgreSQL Installation
- [ ] Installed PostgreSQL 15
  - macOS: `brew install postgresql@15`
  - Windows: Downloaded from postgresql.org
  - Linux: `sudo apt install postgresql`
- [ ] Started PostgreSQL service
  - macOS: `brew services start postgresql@15`
  - Linux: `sudo systemctl start postgresql`
  - Windows: Started via Services
- [ ] Created database `news_db`
  ```sql
  CREATE DATABASE news_db;
  ```
- [ ] Created user `news_user` with password
  ```sql
  CREATE USER news_user WITH PASSWORD 'your_password';
  GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;
  ```
- [ ] Granted schema privileges (PostgreSQL 15+)
  ```sql
  \c news_db
  GRANT ALL ON SCHEMA public TO news_user;
  ```
- [ ] Tested connection works
  ```bash
  psql -h localhost -U news_user -d news_db
  ```

**Your Postgres credentials:**
- Host: `_______________`
- Port: `_______________`
- Database: `_______________`
- User: `_______________`
- Password: `_______________`

---

## ✅ Environment Configuration

- [ ] Copied template to create `.env` file
  ```bash
  cp setup/sample.env notebooks/.env
  ```
- [ ] Edited `notebooks/.env` with actual values
- [ ] Filled in all 7 required variables:
  - [ ] `NEWS_API_KEY`
  - [ ] `OPENAI_API_KEY`
  - [ ] `PGHOST`
  - [ ] `PGPORT`
  - [ ] `PGDATABASE`
  - [ ] `PGUSER`
  - [ ] `PGPASSWORD`
- [ ] Verified `.env` is in `.gitignore` (never commit secrets!)
- [ ] No placeholder values remain (e.g., `your_key_here`)

---

## ✅ Verification Tests

Run these commands to verify each component:

### Test 1: Python Environment
```bash
python --version
# Should show: Python 3.8.x or higher
```
- [ ] Python version ≥ 3.8

### Test 2: Dependencies
```bash
python -c "import pandas, openai, psycopg, pydantic, requests; print('✅ All imports work')"
```
- [ ] All imports successful

### Test 3: Environment Variables
```bash
python -c "from dotenv import load_dotenv; load_dotenv('notebooks/.env'); import os; print('NEWS_API_KEY:', 'SET' if os.getenv('NEWS_API_KEY') else 'MISSING')"
```
- [ ] Environment variables loading correctly

### Test 4: NewsAPI Connection
```bash
python -c "
import requests, os
from dotenv import load_dotenv
load_dotenv('notebooks/.env')
api_key = os.getenv('NEWS_API_KEY')
r = requests.get(f'https://newsapi.org/v2/everything?q=test&pageSize=1&apiKey={api_key}')
print('✅ NewsAPI works' if r.status_code == 200 else f'❌ Error: {r.status_code}')
"
```
- [ ] NewsAPI returns 200 OK

### Test 5: OpenAI Connection
```bash
python -c "
import openai, os
from dotenv import load_dotenv
load_dotenv('notebooks/.env')
openai.api_key = os.getenv('OPENAI_API_KEY')
models = openai.models.list()
print(f'✅ OpenAI connected - {len(models.data)} models available')
"
```
- [ ] OpenAI API connected

### Test 6: PostgreSQL Connection
```bash
python -c "
import psycopg, os
from dotenv import load_dotenv
load_dotenv('notebooks/.env')
conn = psycopg.connect(
    host=os.getenv('PGHOST'),
    port=os.getenv('PGPORT'),
    dbname=os.getenv('PGDATABASE'),
    user=os.getenv('PGUSER'),
    password=os.getenv('PGPASSWORD')
)
print('✅ PostgreSQL connected')
conn.close()
"
```
- [ ] PostgreSQL connection successful

### Test 7: Full Verification
```bash
python verify_setup.py
```
- [ ] All checks pass

---

## ✅ Ready to Start!

Once all items above are checked:

### For Interactive Learning:
```bash
cd notebooks/
jupyter lab

# Open and run:
# - 8_guide.ipynb (Tesla pipeline)
# - 8_lab.ipynb (Disney pipeline)
```

### For Code Examples:
```bash
# From ch08 directory
python listing/8_1.py  # Extract articles
python listing/8_2.py  # AI transformation
python listing/8_3.py  # Enrichment
python listing/8_4_8_5.py  # Schema + Load
```

---

## 📊 Expected Results

After running the guide notebook, you should have:

1. **Terminal output showing:**
   - "Extracted X news articles"
   - "Extracted and analyzed 5 articles"
   - "Enriched 5 articles with quality checks"
   - "Table created successfully"
   - "Inserted 5 rows into news_articles"

2. **Data in PostgreSQL:**
   ```bash
   psql -h localhost -U news_user -d news_db -c "SELECT COUNT(*) FROM news_articles;"
   # Should show: count > 0
   ```

3. **Queryable results:**
   - Articles with sentiment scores
   - Topic classifications
   - Region assignments
   - Multiple timezone conversions

---

## 🆘 If Something Doesn't Work

### Stop and Check:

1. **Which step failed?** Note the exact error message
2. **Check the logs** - Errors usually indicate what's wrong
3. **Verify that specific component:**
   - NewsAPI issue? Test API key at https://newsapi.org/account
   - OpenAI issue? Check billing at https://platform.openai.com/account/billing
   - PostgreSQL issue? Test connection: `psql -h localhost -U news_user -d news_db`

### Get Help:

- **Detailed PostgreSQL help**: `setup/postgres_setup.md`
- **Full chapter documentation**: `../README.md`
- **Airflow setup** (if using): `airflow_project/GETTING_STARTED.md`

---

## 🎯 Success Criteria

You're 100% ready when you can:

1. ✅ Run `python verify_setup.py` → All checks pass
2. ✅ Execute `python listing/8_1.py` → Extracts articles successfully
3. ✅ Open `8_guide.ipynb` → All cells run without errors
4. ✅ Query database → `SELECT COUNT(*) FROM news_articles;` returns data

---

**Once all items are checked, you're ready to build multi-agent AI pipelines! 🎉**

**Start here:** `notebooks/8_guide.ipynb`

