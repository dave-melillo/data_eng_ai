"""
World Series Game 7 Play-by-Play Analysis Pipeline
===================================================
Processes play-by-play text data from World Series Game 7 and extracts:
- Structured game data (innings, scores, players, pitch data)
- Canonical player/pitch mappings
- Excitement metrics and key moments
- Statistical analyses

Configuration:
- NUM_ROWS: Set to 10 for testing, 0 for all rows
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import hashlib
import openai
import os
from pydantic import BaseModel
from typing import Optional
import pickle

# =============================================================================
# CONFIGURATION - CHANGE THIS TO CONTROL NUMBER OF ROWS PROCESSED
# =============================================================================
NUM_ROWS = 10  # Set to 10 for testing, 0 to process ALL rows (729)
# =============================================================================

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 11, 22),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'world_series_analysis',
    default_args=default_args,
    description='Analyze World Series Game 7 play-by-play data with AI',
    schedule_interval=None,  # Manual trigger only
    catchup=False,
    tags=['baseball', 'ai', 'analysis'],
)

# Paths
DATA_PATH = '/opt/airflow/dags/../data/world_series_2025_game_7_playbyplay.csv'
TEMP_DATA_PATH = '/opt/airflow/airflow-data/temp_data.pkl'

# OpenAI setup
openai.api_key = os.getenv('OPENAI_API_KEY')


# =============================================================================
# TASK 1: Load CSV and Create Canonical IDs (9.1)
# =============================================================================
def load_csv_and_create_ids(**context):
    """Load CSV and create play_id and play_hash"""
    print(f"Loading CSV from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    
    # Limit rows if configured
    if NUM_ROWS > 0:
        df = df.head(NUM_ROWS)
        print(f"LIMITED TO {NUM_ROWS} ROWS FOR TESTING")
    else:
        print(f"PROCESSING ALL {len(df)} ROWS")
    
    # Create canonical IDs
    df['play_id'] = range(1, len(df) + 1)
    
    def create_text_hash(text):
        return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]
    
    df['play_hash'] = df['playbyplay'].apply(create_text_hash)
    
    print(f"✅ Loaded {len(df)} plays with canonical IDs")
    
    # Save to temp file for next task
    df.to_pickle(TEMP_DATA_PATH)
    
    return f"Loaded {len(df)} plays"


# =============================================================================
# TASK 2: Extract Structured Data (9.2)
# =============================================================================
class PlayByPlayExtraction(BaseModel):
    inning_number: int
    inning_half: str
    outs: Optional[int] = None
    score_home: Optional[int] = None
    score_away: Optional[int] = None
    pitcher_name: str
    batter_name: str
    runners_on_base: Optional[str] = None
    pre_pitch_balls: Optional[int] = None
    pre_pitch_strikes: Optional[int] = None
    post_pitch_balls: Optional[int] = None
    post_pitch_strikes: Optional[int] = None
    pitch_type: Optional[str] = None
    pitch_velocity_mph: Optional[float] = None
    pitch_result: Optional[str] = None
    ball_in_play: Optional[bool] = None


def extract_structured_data(**context):
    """Extract structured baseball data using OpenAI"""
    df = pd.read_pickle(TEMP_DATA_PATH)
    
    system_prompt = """
You are a baseball play-by-play data extraction assistant. Extract structured information from baseball commentary text.

Extract the following fields:
- inning_number: Numeric inning number (e.g., 1, 2, 3)
- inning_half: "Top" or "Bottom"
- outs: Number of outs at the moment (0, 1, or 2)
- score_home: Home team runs before this play
- score_away: Away team (visiting team) runs before this play
- pitcher_name: Full name of the pitcher (e.g., "Max Scherzer")
- batter_name: Full name of the batter (e.g., "Shohei Ohtani")
- runners_on_base: Comma-separated bases occupied (e.g., "1B", "1B,2B", "1B,3B", "None" if bases empty)
- pre_pitch_balls: Ball count before the pitch (0-3)
- pre_pitch_strikes: Strike count before the pitch (0-2)
- post_pitch_balls: Ball count after the pitch if determinable
- post_pitch_strikes: Strike count after the pitch if determinable
- pitch_type: Type of pitch (e.g., "four-seam fastball", "slider", "curveball", "changeup", "splitter")
- pitch_velocity_mph: Velocity in mph if provided (as a number)
- pitch_result: Immediate outcome (e.g., "Ball", "Strike", "Foul", "In play", "Hit by pitch", "Walk")
- ball_in_play: True if ball was put in play, False otherwise

Rules:
- If information is not available in the text, return null/None
- For runners_on_base, use "None" if bases are empty
- Visiting team is "away", home team is "home"
- Extract names exactly as mentioned in the text
- Be precise with counts - distinguish between pre-pitch and post-pitch counts

Return the result as a JSON object matching the PlayByPlayExtraction structure.
"""
    
    extracted_data = []
    print(f"🔄 Extracting data from {len(df)} plays...")
    
    for idx, row in df.iterrows():
        try:
            completion = openai.beta.chat.completions.parse(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": row['playbyplay']}
                ],
                response_format=PlayByPlayExtraction
            )
            extracted_data.append(completion.choices[0].message.parsed.model_dump())
        except Exception as e:
            print(f"❌ Error processing play_id {row['play_id']}: {e}")
            extracted_data.append({field: None for field in PlayByPlayExtraction.__fields__})
            continue
    
    # Merge extracted data back
    df_extracted = pd.DataFrame(extracted_data)
    df_extracted['play_id'] = df['play_id'].values
    df_extracted['play_hash'] = df['play_hash'].values
    
    df_enriched = df.merge(df_extracted, on=['play_id', 'play_hash'], how='left')
    
    print(f"✅ Successfully extracted data from {len(df_extracted)} plays")
    df_enriched.to_pickle(TEMP_DATA_PATH)
    
    return f"Extracted {len(df_extracted)} plays"


# =============================================================================
# TASK 3: Map to Canonical IDs (9.3)
# =============================================================================
# Reference data
pitcher_reference = {
    28976: "Max Scherzer", 39832: "Shohei Ohtani", 4417203: "Justin Wrobleski",
    33190: "Tyler Glasnow", 4917888: "Louis Varland", 33148: "Chris Bassitt",
    4949041: "Trey Yesavage", 4417806: "Emmet Sheehan", 33841: "Jeff Hoffman",
    33748: "Blake Snell", 4872587: "Yoshinobu Yamamoto", 37793: "Seranthony Dominguez",
    40912: "Shane Bieber"
}

batter_reference = {
    39832: "Shohei Ohtani", 38309: "Will Smith", 30193: "Freddie Freeman",
    33039: "Mookie Betts", 32078: "George Springer", 35682: "Nathan Lukes",
    35002: "Vladimir Guerrero Jr.", 33303: "Max Muncy", 33377: "Teoscar Hernandez",
    39907: "Tommy Edman", 38904: "Bo Bichette", 4997589: "Addison Barger",
    42081: "Alejandro Kirk", 40963: "Daulton Varsho", 41287: "Ernie Clement",
    37729: "Andres Gimenez", 31358: "Enrique Hernandez", 30791: "Miguel Rojas",
    4997181: "Davis Schneider", 42468: "Andy Pages", 39105: "Myles Straw",
    33572: "Isiah Kiner-Falefa"
}

pitch_type_reference = {
    "FC": "Cutter", "FF": "Four-seam FB", "CH": "Changeup", "CU": "Curve",
    "SL": "Slider", "ST": "Sweeper", "FS": "Splitter", "SI": "Sinker",
    "KC": "Knuckle Curve"
}


class PlayerMapping(BaseModel):
    canonical_id: int
    canonical_name: str
    confidence: str


class PitchTypeMapping(BaseModel):
    canonical_abbr: str
    canonical_text: str
    confidence: str


def map_to_canonical_ids(**context):
    """Map extracted names and pitch types to canonical IDs"""
    df_enriched = pd.read_pickle(TEMP_DATA_PATH)
    
    # Create prompts
    pitcher_str = "\\n".join([f"ID: {pid}, Name: {name}" for pid, name in pitcher_reference.items()])
    pitcher_prompt = f"""
You are a baseball data quality expert. Match the provided pitcher name to the correct canonical pitcher from this list:

{pitcher_str}

Rules:
- Match based on last name, full name, or any reasonable variation
- Examples: "Scherzer" should match "Max Scherzer", "Ohtani" should match "Shohei Ohtani"
- Return the canonical_id and canonical_name from the list above
- Set confidence to "high" for exact matches, "medium" for last name only, "low" for uncertain matches
- If no reasonable match exists, use the closest match and set confidence to "low"

Return a JSON object with: canonical_id (int), canonical_name (str), confidence (str)
"""
    
    batter_str = "\\n".join([f"ID: {bid}, Name: {name}" for bid, name in batter_reference.items()])
    batter_prompt = f"""
You are a baseball data quality expert. Match the provided batter name to the correct canonical batter from this list:

{batter_str}

Rules:
- Match based on last name, full name, or any reasonable variation
- Examples: "Guerrero" should match "Vladimir Guerrero Jr.", "Springer" should match "George Springer"
- Return the canonical_id and canonical_name from the list above
- Set confidence to "high" for exact matches, "medium" for last name only, "low" for uncertain matches
- If no reasonable match exists, use the closest match and set confidence to "low"

Return a JSON object with: canonical_id (int), canonical_name (str), confidence (str)
"""
    
    pitch_str = "\\n".join([f"Abbr: {abbr}, Text: {text}" for abbr, text in pitch_type_reference.items()])
    pitch_type_prompt = f"""
You are a baseball data quality expert. Match the provided pitch type to the correct canonical pitch type from this list:

{pitch_str}

Rules:
- Match based on common pitch terminology and abbreviations
- Examples: "fastball" or "four-seam fastball" → "Four-seam FB" (FF)
- "curve" or "curveball" → "Curve" (CU)
- "slider" → "Slider" (SL)
- Handle variations like "four seam fastball", "4-seam FB", etc.
- Return the canonical_abbr and canonical_text from the list above
- Set confidence to "high" for clear matches, "medium" for likely matches, "low" for uncertain
- If null/None provided, return null values with low confidence

Return a JSON object with: canonical_abbr (str), canonical_text (str), confidence (str)
"""
    
    print(f"🔄 Mapping to canonical IDs for {len(df_enriched)} plays...")
    
    pitcher_mappings = []
    batter_mappings = []
    pitch_type_mappings = []
    
    for idx, row in df_enriched.iterrows():
        # Map pitcher
        if pd.notna(row['pitcher_name']):
            try:
                completion = openai.beta.chat.completions.parse(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": pitcher_prompt},
                        {"role": "user", "content": f"Pitcher name: {row['pitcher_name']}"}
                    ],
                    response_format=PlayerMapping
                )
                pitcher_mappings.append(completion.choices[0].message.parsed.model_dump())
            except Exception as e:
                print(f"❌ Error mapping pitcher: {e}")
                pitcher_mappings.append({"canonical_id": None, "canonical_name": None, "confidence": "low"})
        else:
            pitcher_mappings.append({"canonical_id": None, "canonical_name": None, "confidence": "low"})
        
        # Map batter
        if pd.notna(row['batter_name']):
            try:
                completion = openai.beta.chat.completions.parse(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": batter_prompt},
                        {"role": "user", "content": f"Batter name: {row['batter_name']}"}
                    ],
                    response_format=PlayerMapping
                )
                batter_mappings.append(completion.choices[0].message.parsed.model_dump())
            except Exception as e:
                print(f"❌ Error mapping batter: {e}")
                batter_mappings.append({"canonical_id": None, "canonical_name": None, "confidence": "low"})
        else:
            batter_mappings.append({"canonical_id": None, "canonical_name": None, "confidence": "low"})
        
        # Map pitch type
        if pd.notna(row['pitch_type']):
            try:
                completion = openai.beta.chat.completions.parse(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": pitch_type_prompt},
                        {"role": "user", "content": f"Pitch type: {row['pitch_type']}"}
                    ],
                    response_format=PitchTypeMapping
                )
                pitch_type_mappings.append(completion.choices[0].message.parsed.model_dump())
            except Exception as e:
                print(f"❌ Error mapping pitch type: {e}")
                pitch_type_mappings.append({"canonical_abbr": None, "canonical_text": None, "confidence": "low"})
        else:
            pitch_type_mappings.append({"canonical_abbr": None, "canonical_text": None, "confidence": "low"})
    
    # Add mapped columns
    df_enriched['pitcher_id'] = [m['canonical_id'] for m in pitcher_mappings]
    df_enriched['pitcher_canonical_name'] = [m['canonical_name'] for m in pitcher_mappings]
    df_enriched['pitcher_confidence'] = [m['confidence'] for m in pitcher_mappings]
    
    df_enriched['batter_id'] = [m['canonical_id'] for m in batter_mappings]
    df_enriched['batter_canonical_name'] = [m['canonical_name'] for m in batter_mappings]
    df_enriched['batter_confidence'] = [m['confidence'] for m in batter_mappings]
    
    df_enriched['pitch_type_abbr'] = [m['canonical_abbr'] for m in pitch_type_mappings]
    df_enriched['pitch_type_canonical'] = [m['canonical_text'] for m in pitch_type_mappings]
    df_enriched['pitch_type_confidence'] = [m['confidence'] for m in pitch_type_mappings]
    
    print(f"✅ Successfully mapped canonical IDs")
    
    df_enriched.to_pickle(TEMP_DATA_PATH)
    return f"Mapped {len(df_enriched)} plays"


# =============================================================================
# TASK 4: Advanced Transformations (9.4)
# =============================================================================
class PlayAnalysis(BaseModel):
    key_moment: bool
    excitement: int


def analyze_excitement_and_key_moments(**context):
    """Analyze each play for excitement and key moments"""
    df_enriched = pd.read_pickle(TEMP_DATA_PATH)
    
    system_prompt = """
You are a baseball narrative analyst. Analyze the provided play-by-play commentary and determine:

1. **key_moment** (boolean): Is this a key moment in the game?
   - TRUE for: home runs, game-tying hits, go-ahead runs, critical strikeouts, bases-loaded situations, 
     double plays that end threats, extra-inning plays, close game situations, defensive gems
   - TRUE for: any play where the commentary suggests high stakes, tension, or game-changing impact
   - FALSE for: routine outs, standard balls/strikes, typical fly outs, grounders with no drama
   - Look for phrases like "crucial", "pivotal", "clutch", "ties the game", "takes the lead", etc.

2. **excitement** (integer 1-10): Rate the excitement level of this play
   - 1-2: Routine play, minimal drama (standard out, foul ball, ball/strike)
   - 3-4: Somewhat notable (base hit, walk, strikeout in normal situation)
   - 5-6: Moderately exciting (extra-base hit, key defensive play, close play at base)
   - 7-8: Very exciting (home run, bases loaded, clutch hit, game-changing play)
   - 9-10: Extremely exciting (walk-off hit, game-tying homer, incredible defensive play, high-stakes moment)
   
Consider factors:
- Score situation (close game = higher excitement)
- Inning (later innings = higher stakes)
- Base runners (more runners = more tension)
- Outs (2 outs = more pressure)
- Game impact (does this change the score or game state significantly?)
- Commentary tone (exclamation marks, dramatic language = higher excitement)

Return a JSON object with: key_moment (bool), excitement (int 1-10)
"""
    
    print(f"🔄 Analyzing excitement and key moments...")
    
    play_analyses = []
    for idx, row in df_enriched.iterrows():
        try:
            completion = openai.beta.chat.completions.parse(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": row['playbyplay']}
                ],
                response_format=PlayAnalysis
            )
            play_analyses.append(completion.choices[0].message.parsed.model_dump())
        except Exception as e:
            print(f"❌ Error analyzing play: {e}")
            play_analyses.append({"key_moment": False, "excitement": 1})
            continue
    
    df_enriched['key_moment'] = [a['key_moment'] for a in play_analyses]
    df_enriched['excitement'] = [a['excitement'] for a in play_analyses]
    
    print(f"✅ Successfully analyzed {len(play_analyses)} plays")
    
    df_enriched.to_pickle(TEMP_DATA_PATH)
    return f"Analyzed {len(play_analyses)} plays"


# =============================================================================
# TASK 5: Generate Summary Statistics (9.5)
# =============================================================================
def generate_summary_statistics(**context):
    """Generate final summary statistics"""
    df_enriched = pd.read_pickle(TEMP_DATA_PATH)
    
    # Excitement statistics
    key_moments_count = df_enriched['key_moment'].sum()
    avg_excitement = df_enriched['excitement'].mean()
    
    # Pitcher statistics
    pitcher_analysis = df_enriched[df_enriched['pitcher_id'].notna()].copy()
    pitcher_stats = pitcher_analysis.groupby(['pitcher_id', 'pitcher_canonical_name']).agg({
        'pitch_velocity_mph': 'mean',
        'pitch_type_canonical': lambda x: x.value_counts().index[0] if len(x.value_counts()) > 0 else None,
        'play_id': 'count'
    }).reset_index()
    pitcher_stats.columns = ['pitcher_id', 'pitcher_name', 'avg_pitch_speed_mph', 'most_frequent_pitch', 'total_pitches']
    
    # Batter statistics
    batter_analysis = df_enriched[df_enriched['batter_id'].notna()].copy()
    batter_stats = batter_analysis.groupby(['batter_id', 'batter_canonical_name']).agg({
        'post_pitch_balls': lambda x: x.sum() if x.notna().any() else 0,
        'post_pitch_strikes': lambda x: x.sum() if x.notna().any() else 0,
        'ball_in_play': lambda x: x.sum() if x.notna().any() else 0,
        'play_id': 'count'
    }).reset_index()
    batter_stats.columns = ['batter_id', 'batter_name', 'total_balls', 'total_strikes', 'balls_in_play', 'plate_appearances']
    
    summary = f"""
    ================================================================================
    WORLD SERIES GAME 7 ANALYSIS COMPLETE
    ================================================================================
    
    📊 Data Processed: {len(df_enriched)} plays
    
    🎭 Excitement Analysis:
       - Average excitement: {avg_excitement:.2f}/10
       - Key moments: {key_moments_count} ({(key_moments_count/len(df_enriched)*100):.1f}%)
    
    ⚾ Pitcher Analysis:
       - Unique pitchers: {len(pitcher_stats)}
       - Total pitches: {pitcher_stats['total_pitches'].sum()}
    
    🏏 Batter Analysis:
       - Unique batters: {len(batter_stats)}
       - Total plate appearances: {batter_stats['plate_appearances'].sum()}
    
    ✅ Pipeline Complete!
    ================================================================================
    """
    
    print(summary)
    
    return summary


# =============================================================================
# Define Tasks
# =============================================================================
task_load = PythonOperator(
    task_id='load_csv_and_create_ids',
    python_callable=load_csv_and_create_ids,
    dag=dag,
)

task_extract = PythonOperator(
    task_id='extract_structured_data',
    python_callable=extract_structured_data,
    dag=dag,
)

task_map = PythonOperator(
    task_id='map_to_canonical_ids',
    python_callable=map_to_canonical_ids,
    dag=dag,
)

task_analyze = PythonOperator(
    task_id='analyze_excitement_key_moments',
    python_callable=analyze_excitement_and_key_moments,
    dag=dag,
)

task_summary = PythonOperator(
    task_id='generate_summary_statistics',
    python_callable=generate_summary_statistics,
    dag=dag,
)

# Set dependencies
task_load >> task_extract >> task_map >> task_analyze >> task_summary

