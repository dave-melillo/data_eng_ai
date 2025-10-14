# 🚀 Airflow News Pipeline - START HERE

Welcome! This is a complete, working Airflow setup for your Data Engineering course.

---

## ⚡ Super Quick Start

```bash
# 1. Create your config
cp env.template .env
# Edit .env with your API keys

# 2. Start Airflow
./quickstart.sh

# 3. Open browser
# http://localhost:8080
# Login: airflow / airflow
```

**That's it!** Your Airflow pipeline is ready to run.

---

## 📚 Which Guide Should I Read?

### 🆕 Never used Airflow before?
👉 Read **[GETTING_STARTED.md](GETTING_STARTED.md)**
- Assumes zero knowledge
- Step-by-step instructions
- Includes PostgreSQL setup
- Quick troubleshooting

### 🔍 Need detailed reference?
👉 Read **[SETUP_GUIDE.md](SETUP_GUIDE.md)**
- Complete CLI commands
- Advanced usage
- Comprehensive troubleshooting
- Performance optimization

### 📖 Just want overview?
👉 Read **[README.md](README.md)**
- Quick project overview
- Common commands
- File structure

---

## 🎯 What This Pipeline Does

```
Extract articles (NewsAPI)
    ↓
Transform with AI (OpenAI)
    ↓
Categorize & Enrich (AI)
    ↓
Load to PostgreSQL
    ↓
Verify
```

**Result:** Enriched news articles in your database with sentiment scores, topics, and regional classifications!

---

## 🏃 Running Your First Pipeline

**After starting Airflow:**

### Option 1: Default Parameters (Tesla, yesterday-today)
In UI: Click ▶️ → "Trigger DAG"

### Option 2: Custom Parameters (Recommended)
```bash
# Get container name
docker ps | grep airflow

# Trigger with your parameters
docker exec -it <container_name> airflow dags trigger news_articles_pipeline \
  --conf '{"query": "Apple", "from_date": "2025-10-01", "to_date": "2025-10-08"}'
```

**Replace `<container_name>` with the actual name** (usually `airflow_project_airflow_1`)

---

## 📋 Files You Need

**You provide:**
- `.env` (copy from `env.template` and fill in your credentials)

**We provide:**
- Everything else! Just run `./quickstart.sh`

---

## ❓ Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't connect to PostgreSQL | Use `PGHOST=host.docker.internal` in `.env` |
| DAG not showing | Wait 30 seconds, refresh browser |
| Invalid API key | Check `.env`, restart: `docker compose restart` |
| Container not running | Run `./quickstart.sh` |

**More help?** See [SETUP_GUIDE.md](SETUP_GUIDE.md#troubleshooting)

---

## 🎓 For Students

This project teaches:
- ✅ Airflow workflow orchestration
- ✅ ETL pipeline design
- ✅ AI integration in data pipelines
- ✅ Production data engineering practices
- ✅ Docker containerization

**Time required:**
- First-time setup: ~30 minutes
- Running pipeline: ~5 minutes
- Exploring results: ~10 minutes

---

## 🆘 Need Help?

1. Check the [Troubleshooting](#quick-troubleshooting) section above
2. Read **[GETTING_STARTED.md](GETTING_STARTED.md)** for detailed steps
3. Consult **[SETUP_GUIDE.md](SETUP_GUIDE.md)** for advanced help
4. View logs: `docker compose logs -f`

---

**Ready? Run `./quickstart.sh` and let's go!** 🚀

