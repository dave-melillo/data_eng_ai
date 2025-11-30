# 🚀 World Series Analysis Pipeline - START HERE

Analyzes World Series Game 7 play-by-play data using AI to extract structured information, player stats, and excitement metrics.

---

## ⚡ Super Quick Start

👉 **READ THIS FIRST:** [QUICK_START.md](QUICK_START.md) ⭐

**3 Steps:**
```bash
# 1. Configure
cp env.template .env
# Edit .env - add OpenAI API key

# 2. Start Airflow
./quickstart.sh

# 3. Open http://localhost:8080
# Login: airflow / airflow
# Trigger: world_series_analysis
```

**That's it!** The pipeline will analyze Game 7 data.

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
Extract data
    ↓
Transform with AI
    ↓
Enrich & Analyze
    ↓
Load to Database
    ↓
Verify
```

**Result:** Clean, enriched data in your PostgreSQL database ready for analysis!

---

## 🏃 Running Your First Pipeline

**After starting Airflow:**

### Option 1: Default Parameters
In UI: Click ▶️ → "Trigger DAG"

### Option 2: Custom Parameters (CLI)
```bash
# Get container name
docker ps | grep airflow

# Trigger with your parameters
docker exec -it <container_name> airflow dags trigger your_dag_name
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


