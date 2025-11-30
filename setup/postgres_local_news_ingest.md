## Local Postgres Setup for News Ingest (Beginner Friendly)

This guide sets up a local PostgreSQL database and credentials to load the `enriched_df` from `ch08/8scratch.ipynb`.

### 1) Install PostgreSQL (macOS)
- Using Homebrew:
```sh
brew install postgresql@16
brew services start postgresql@16
psql --version
```

If you don’t use Homebrew, download the macOS installer from `https://www.postgresql.org/download/macosx/` and follow the defaults.

### 2) Create Role and Database
Run these once to create a dedicated user and database for this exercise.

Option A: Terminal helpers (recommended):
```sh
createuser -U postgres -h localhost --pwprompt news_user
# Enter a strong password when prompted (remember it)
createdb -U postgres -h localhost --owner=news_user news_db
```

Option B: Using psql:
```sh
psql postgres
-- Inside psql
CREATE ROLE news_user WITH LOGIN PASSWORD 'REPLACE_ME_STRONG_PASSWORD';
CREATE DATABASE news_db OWNER news_user;
GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;
\\q
```

### 3) Set Environment Variables
Add these to your project `.env` (used by the notebook via `load_dotenv()`):
```
PGHOST=localhost
PGPORT=5432
PGDATABASE=news_db
PGUSER=news_user
PGPASSWORD=REPLACE_ME_STRONG_PASSWORD
```

Notes:
- If you installed a different Postgres version, port 5432 is still the default unless changed.
- If authentication fails, check `pg_hba.conf` (macOS Homebrew path often under `/opt/homebrew/var/postgresql@16/pg_hba.conf`). Ensure a line exists like:
```
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
```
Then restart: `brew services restart postgresql@16`.

### 4) Test Connectivity
From terminal:
```sh
PGPASSWORD=$PGPASSWORD psql -h $PGHOST -p $PGPORT -U $PGUSER -d $PGDATABASE -c "SELECT current_user, current_database();"
```

From Python (inside your project venv / notebook kernel):
```python
import os, sys, subprocess
try:
    import psycopg
except Exception:
    subprocess.run([sys.executable, "-m", "pip", "install", "psycopg[binary]>=3.1"], check=False)
    import psycopg

with psycopg.connect(
    host=os.getenv("PGHOST"),
    port=os.getenv("PGPORT"),
    dbname=os.getenv("PGDATABASE"),
    user=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        print(cur.fetchone())
```

### 5) Table Creation & Loading
The notebook will:
- Generate a `CREATE TABLE` DDL via AI, store it as a variable, and execute it.
- Batch-insert rows from `enriched_df` into the target table using `psycopg`.

You are ready to run the notebook cell that creates the table and loads the data.


