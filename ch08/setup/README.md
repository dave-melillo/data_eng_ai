# Chapter 8 Setup Resources

This directory contains everything you need to configure your environment for the Chapter 8 multi-agent news pipeline.

---

## 📚 Setup Files Overview

| File | Purpose | When to Use |
|------|---------|-------------|
| **QUICK_START.md** | Step-by-step setup guide | Start here if you're new |
| **postgres_setup.md** | Complete PostgreSQL setup | Detailed database configuration |
| **SETUP_CHECKLIST.md** | Interactive checklist | Track your setup progress |
| **sample.env** | Environment variables template | Copy and fill with your credentials |

---

## 🚀 Recommended Setup Flow

### For Beginners (First Time)

1. **Start Here** → Read `QUICK_START.md`
   - 15-minute guided setup
   - Step-by-step instructions
   - All prerequisites explained

2. **Configure Database** → Follow `postgres_setup.md`
   - Choose: Cloud (Supabase) or Local installation
   - Create database and user
   - Test connection

3. **Track Progress** → Use `SETUP_CHECKLIST.md`
   - Check off each completed item
   - Verify each component works
   - Ensure nothing is missed

4. **Configure Environment** → Copy `sample.env`
   ```bash
   # From ch08 directory:
   cp setup/sample.env notebooks/.env
   # Edit notebooks/.env with your actual credentials
   ```

5. **Verify Setup** → Run verification script
   ```bash
   # From ch08 directory:
   python verify_setup.py
   ```

### For Experienced Users (Quick Setup)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up PostgreSQL (choose one):
#    Option A: Use Supabase (https://supabase.com)
#    Option B: Local install + create database

# 3. Configure environment
cp setup/sample.env notebooks/.env
# Edit notebooks/.env with your keys

# 4. Verify
python verify_setup.py
```

---

## 🔑 Required Credentials

You need **3 sets of credentials**:

### 1. NewsAPI (FREE)
- **Where:** https://newsapi.org/
- **What:** API key for news article extraction
- **Cost:** Free (100 requests/day)
- **Setup time:** 2 minutes

### 2. OpenAI API (PAID)
- **Where:** https://platform.openai.com/
- **What:** API key for AI agents
- **Cost:** ~$5-10 for all chapter exercises
- **Setup time:** 5 minutes
- **Note:** Requires payment method

### 3. PostgreSQL Database
- **Where:** Supabase (cloud) or local installation
- **What:** Database credentials (host, port, database, user, password)
- **Cost:** Free (Supabase free tier or local)
- **Setup time:** 5-15 minutes

---

## 📋 Environment Variables Reference

All pipelines require these 7 variables:

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `NEWS_API_KEY` | Your NewsAPI key | `a1b2c3d4e5f6...` |
| `OPENAI_API_KEY` | Your OpenAI key | `sk-proj-xyz...` |
| `PGHOST` | Database host | `localhost` or `db.xxx.supabase.co` |
| `PGPORT` | Database port | `5432` |
| `PGDATABASE` | Database name | `news_db` or `postgres` |
| `PGUSER` | Database user | `news_user` or `postgres` |
| `PGPASSWORD` | Database password | Your secure password |

**Where to put them:**
- For **notebooks**: `ch08/notebooks/.env`
- For **listings**: `ch08/.env`
- For **Airflow**: `ch08/airflow_project/.env`

---

## 🧪 Testing Your Setup

### Quick Tests (Individual Components)

```bash
# Test NewsAPI
python -c "import requests, os; from dotenv import load_dotenv; load_dotenv('notebooks/.env'); r=requests.get(f'https://newsapi.org/v2/everything?q=test&pageSize=1&apiKey={os.getenv(\"NEWS_API_KEY\")}'); print('✅ NewsAPI works' if r.status_code==200 else '❌ Failed')"

# Test OpenAI
python -c "import openai, os; from dotenv import load_dotenv; load_dotenv('notebooks/.env'); openai.api_key=os.getenv('OPENAI_API_KEY'); models=openai.models.list(); print(f'✅ OpenAI works - {len(models.data)} models')"

# Test PostgreSQL
python -c "import psycopg, os; from dotenv import load_dotenv; load_dotenv('notebooks/.env'); conn=psycopg.connect(host=os.getenv('PGHOST'),port=os.getenv('PGPORT'),dbname=os.getenv('PGDATABASE'),user=os.getenv('PGUSER'),password=os.getenv('PGPASSWORD')); print('✅ PostgreSQL connected'); conn.close()"
```

### Complete Verification

```bash
# Run comprehensive verification script
python verify_setup.py

# Should show:
# ✅ Python Version
# ✅ Dependencies  
# ✅ Environment Files
# ✅ Environment Variables
# ✅ NewsAPI Connection
# ✅ OpenAI Connection
# ✅ PostgreSQL Connection
# ✅ Pipeline Test
# 
# 🎉 ALL CHECKS PASSED!
```

---

## 🆘 Troubleshooting

### Issue: "verify_setup.py fails on NewsAPI"

**Causes:**
- Invalid API key
- No internet connection  
- Rate limit exceeded (100/day)

**Solution:**
1. Verify key at https://newsapi.org/account
2. Check you copied the key correctly
3. Ensure no extra spaces in `.env` file

### Issue: "verify_setup.py fails on OpenAI"

**Causes:**
- Invalid API key
- No payment method on file
- Usage limits exceeded

**Solution:**
1. Check billing: https://platform.openai.com/account/billing
2. Add payment method if needed
3. Verify key starts with `sk-` or `sk-proj-`
4. Generate new key if needed

### Issue: "verify_setup.py fails on PostgreSQL"

**Causes:**
- PostgreSQL not running
- Database doesn't exist
- User lacks privileges
- Wrong credentials in `.env`

**Solution:**
1. See detailed guide: `postgres_setup.md`
2. Verify service running:
   ```bash
   # macOS
   brew services list | grep postgresql
   
   # Linux
   sudo systemctl status postgresql
   ```
3. Test manually: `psql -h localhost -U news_user -d news_db`

### Issue: "Module not found" errors

**Solution:**
```bash
pip install -r requirements.txt

# If still failing, try upgrading pip:
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📖 Documentation Map

### Getting Started
- **QUICK_START.md** ← Start here for guided setup
- **SETUP_CHECKLIST.md** ← Track your progress

### Detailed Guides
- **postgres_setup.md** ← Complete database setup
- **../README.md** ← Full chapter documentation
- **../airflow_project/GETTING_STARTED.md** ← Airflow orchestration (optional)

### Reference
- **sample.env** ← Environment variables template
- **../verify_setup.py** ← Automated verification script

---

## 💡 Pro Tips

### Tip 1: Use Cloud PostgreSQL for Simplicity
Supabase is free and requires no installation:
- Sign up in 2 minutes
- Always accessible
- No local service management
- Perfect for learning

### Tip 2: Set OpenAI Usage Limits
Prevent unexpected bills:
1. Go to https://platform.openai.com/account/limits
2. Set hard limit: $10/month
3. Set soft limit: $5/month (get email warning)

### Tip 3: Create Multiple .env Files
```bash
# For notebooks
cp sample.env ../notebooks/.env

# For root-level listings
cp sample.env ../.env

# Edit both with same credentials
```

### Tip 4: Use Jupyter Lab
Better than Jupyter Notebook:
```bash
pip install jupyterlab
jupyter lab notebooks/8_guide.ipynb
```

### Tip 5: Start Small
- Process 5 articles first (default in notebooks)
- Verify everything works
- Then scale up to 50-100 articles

---

## 🎓 Learning Resources

### Official Documentation
- **NewsAPI Docs**: https://newsapi.org/docs
- **OpenAI Docs**: https://platform.openai.com/docs
- **PostgreSQL Tutorial**: https://www.postgresqltutorial.com/
- **psycopg3 Docs**: https://www.psycopg.org/psycopg3/docs/

### Chapter-Specific
- **Main README**: `../README.md`
- **Notebooks**: `../notebooks/`
- **Code Listings**: `../listing/`
- **Airflow Project**: `../airflow_project/`

---

## ⏱️ Estimated Time Investment

- **Initial Setup**: 15-20 minutes
- **Guide Notebook**: 30-45 minutes
- **Lab Exercise**: 45-60 minutes
- **Airflow Setup** (optional): 30 minutes
- **Total**: 2-3 hours for complete chapter

---

## 🎯 What's Next?

After setup is complete:

1. ✅ **Run Guide** → `notebooks/8_guide.ipynb`
   - Learn multi-agent architecture
   - Build Tesla news pipeline
   - Understand each agent's role

2. ✅ **Complete Lab** → `notebooks/8_lab.ipynb`
   - Build Disney analytics pipeline
   - Add business line categorization
   - Practice custom agent design

3. ✅ **Explore Airflow** → `airflow_project/`
   - Automate the pipeline
   - Schedule daily runs
   - Production deployment patterns

4. ✅ **Customize** → Build your own
   - Different companies
   - Custom categorization
   - Additional agents

---

**Questions?** Check the troubleshooting sections in each guide or refer to the main chapter README.

**Ready?** Run `python verify_setup.py` from the ch08 directory to confirm everything is configured! 🚀

