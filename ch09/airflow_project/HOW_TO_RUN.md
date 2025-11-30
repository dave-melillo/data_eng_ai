# 🎯 HOW TO RUN THE WORLD SERIES ANALYSIS PIPELINE

## Step-by-Step Instructions

### 1️⃣ Setup (First Time Only)

```bash
cd /Users/davemelillo/Desktop/data_eng_ai/ch09/airflow_project

# Create .env file
cp env.template .env

# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-actual-key-here
```

### 2️⃣ Start Airflow

```bash
./quickstart.sh
```

Wait for message: `✅ Airflow is Running!`

### 3️⃣ Open Airflow UI

```
http://localhost:8080
Login: airflow / airflow
```

### 4️⃣ Configure NUM_ROWS (Choose One)

**Option A: Test Mode (10 rows) - RECOMMENDED FIRST**
```python
# Open: dags/world_series_pipeline.py
# Line 28: NUM_ROWS = 10  ✅ Already set!
```
- Time: ~2 minutes
- Cost: ~$0.50
- Perfect for testing!

**Option B: Full Analysis (729 rows)**
```python
# Open: dags/world_series_pipeline.py
# Line 28: NUM_ROWS = 0  ⚠️ Change from 10 to 0
```
- Time: ~15-20 minutes
- Cost: ~$5-7
- Complete analysis!

**After changing NUM_ROWS:**
```bash
docker compose restart
```

### 5️⃣ Run the Pipeline

**In Airflow UI:**
1. Find `world_series_analysis` in DAG list
2. Toggle it ON (if paused)
3. Click ▶️ play button
4. Select "Trigger DAG"
5. Watch the magic happen! 🎉

---

## 📊 View Results

### While Running:
- Click on DAG name → Graph view
- Watch tasks turn green: gray → yellow → green

### After Completion:
1. Click on `generate_summary_statistics` task
2. Click "Logs" button
3. See complete analysis summary!

---

## 🔄 Run Again

**Same settings:**
- Just click ▶️ again in UI

**Different settings:**
1. Edit `NUM_ROWS` in DAG file
2. Run: `docker compose restart`
3. Trigger DAG again

---

## 🛑 Stop Airflow

```bash
docker compose down
```

---

## ⚠️ Important Notes

1. **Always test with NUM_ROWS=10 first!**
   - Fast execution
   - Low cost
   - Validates everything works

2. **Full run (NUM_ROWS=0) takes ~20 minutes**
   - Be patient
   - Watch logs for progress
   - Cost: ~$5-7

3. **Edit NUM_ROWS in DAG file directly**
   - Line 28 of `dags/world_series_pipeline.py`
   - Restart Airflow after changes

---

## 🎓 What You Get

After pipeline completes:

✅ **Structured Data**
- Innings, scores, outs
- Player names
- Pitch types and velocities

✅ **Canonical Mappings**
- Player IDs (handles "Scherzer" → "Max Scherzer")
- Pitch type abbreviations

✅ **Excitement Analysis**
- Excitement rating (1-10) per play
- Key moment identification

✅ **Statistics**
- Pitcher performance (avg speed, pitch types)
- Batter performance (balls, strikes, contact rate)

---

## 📚 Need Help?

- **Quick Setup:** [QUICK_START.md](QUICK_START.md)
- **Beginner Guide:** [GETTING_STARTED.md](GETTING_STARTED.md)
- **Troubleshooting:** [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

**Ready to run?** Follow steps 1-5 above! 🚀⚾

