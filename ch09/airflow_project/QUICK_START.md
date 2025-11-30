# 🚀 World Series Analysis Pipeline - QUICK START

## ⚡ 3-Step Setup (5 minutes)

### 1. Configure Environment
```bash
cd ch09/airflow_project
cp env.template .env
# Edit .env with your OpenAI API key
```

**Required in `.env`:**
```bash
OPENAI_API_KEY=sk-your-key-here
```

### 2. Start Airflow
```bash
./quickstart.sh
```

**First time:** 2-3 minutes  
**After that:** 30-60 seconds

### 3. Run the Pipeline
```bash
# Open browser: http://localhost:8080
# Login: airflow / airflow
# Find: world_series_analysis
# Click: ▶️ Trigger DAG
```

---

## 🎯 What It Does

```
Load CSV (729 plays)
    ↓
Extract Data (innings, scores, players, pitches) [OpenAI]
    ↓
Map to Canonical IDs (clean player/pitch names) [OpenAI]
    ↓
Analyze Excitement & Key Moments [OpenAI]
    ↓
Generate Summary Statistics
```

**Result:** Complete analysis of World Series Game 7!

---

## ⚙️ IMPORTANT: Configure Number of Rows

**For TESTING (10 rows - fast & cheap):**
```python
# In dags/world_series_pipeline.py line 28:
NUM_ROWS = 10  # ✅ Default - processes 10 plays (~2 minutes, ~$0.50)
```

**For FULL ANALYSIS (729 rows - slow & expensive):**
```python
# In dags/world_series_pipeline.py line 28:
NUM_ROWS = 0  # ⚠️ processes ALL 729 plays (~20 minutes, ~$5-7)
```

**After changing NUM_ROWS:**
```bash
docker compose restart  # Restart Airflow to pick up changes
```

---

## 📊 View Results

**In Airflow UI:**
1. Click on `world_series_analysis` DAG
2. Click on latest run
3. Click on `generate_summary_statistics` task
4. Click "Logs" to see full summary

---

## 🛠️ Common Commands

```bash
# Start Airflow
./quickstart.sh

# Stop Airflow
docker compose down

# View logs (for debugging)
docker compose logs -f

# Restart (after changing NUM_ROWS)
docker compose restart

# Stop everything and clean up
docker compose down -v
```

---

## ❓ Troubleshooting

| Problem | Solution |
|---------|----------|
| Pipeline fails | Check OpenAI API key in `.env` |
| "Out of tokens" error | Set NUM_ROWS=10 for testing |
| DAG not showing | Wait 30 seconds, refresh browser |
| Want to process all data | Set NUM_ROWS=0 and restart |

---

## 💰 Cost Estimates

**Testing (10 rows):**
- Processing time: ~2 minutes
- OpenAI cost: ~$0.30-0.50
- Perfect for development!

**Full Analysis (729 rows):**
- Processing time: ~15-20 minutes
- OpenAI cost: ~$5-7
- Use when ready for complete analysis!

---

## 📝 Pipeline Tasks Explained

1. **load_csv_and_create_ids**: Loads CSV, creates play_id and play_hash
2. **extract_structured_data**: Extracts innings, scores, players, pitch data
3. **map_to_canonical_ids**: Maps player names and pitch types to canonical IDs
4. **analyze_excitement_key_moments**: Rates excitement (1-10) and identifies key moments
5. **generate_summary_statistics**: Creates final summary report

---

## 🎓 Tips

- **Always test with NUM_ROWS=10 first!**
- Check logs after each task for errors
- Full analysis takes ~20 minutes - be patient!
- Results include excitement arc, pitcher stats, and batter stats

---

**Ready? Edit `NUM_ROWS` in the DAG, start Airflow, and trigger!** ⚾

