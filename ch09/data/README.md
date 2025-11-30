# Data Directory

This directory contains the CSV data file used by the World Series analysis pipeline.

## File

**`world_series_2025_game_7_playbyplay.csv`**
- 729 plays from World Series Game 7
- Single column: `playbyplay` (text commentary)
- Used by Airflow DAG: `world_series_analysis`

## Pipeline Overview

The Airflow pipeline processes this data through:
1. Loading and ID creation
2. Structured data extraction (AI)
3. Canonical mapping (AI)
4. Excitement analysis (AI)
5. Statistical summary

See `../airflow_project/QUICK_START.md` for setup instructions.

