# PostgreSQL Setup for Chapter 8

This guide will help you set up PostgreSQL for the Chapter 8 notebooks and code listings. The multi-agent news pipeline stores enriched articles in a Postgres database.

## Quick Overview

**What you'll create:**
- Database: `news_db`
- User: `news_user` (with password)
- Table: `news_articles` or `disney_news_articles` (auto-created by the pipeline)

**Time required:** 10-15 minutes for first-time setup

---

## Option 1: Local PostgreSQL (Recommended for Learning)

### macOS Installation

#### Install PostgreSQL using Homebrew

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15

# Verify it's running
brew services list | grep postgresql
```

#### Create Database and User

```bash
# Connect to PostgreSQL as the default user
psql postgres

# Inside the PostgreSQL prompt (postgres=#), run these commands:
```

```sql
-- Create the database
CREATE DATABASE news_db;

-- Create the user with a secure password (CHANGE THIS!)
CREATE USER news_user WITH PASSWORD 'secure_password_123';

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;

-- Connect to the news_db database
\c news_db

-- Grant schema privileges (PostgreSQL 15+ requirement)
GRANT ALL ON SCHEMA public TO news_user;

-- Exit PostgreSQL
\q
```

#### Test Your Connection

```bash
# Try connecting with the new user
psql -h localhost -U news_user -d news_db

# Enter your password when prompted
# You should see: news_db=>

# Test a query
SELECT current_database(), current_user;

# Exit
\q
```

✅ **Success!** If you can connect and run queries, you're all set!

---

### Windows Installation

#### Install PostgreSQL

1. **Download Installer:**
   - Visit: https://www.postgresql.org/download/windows/
   - Download PostgreSQL 15.x installer
   - Run the installer

2. **Installation Wizard:**
   - Accept default installation directory
   - **Remember your superuser (postgres) password!**
   - Use default port: 5432
   - Use default locale

3. **Verify Installation:**
   - Search for "pgAdmin 4" in Start menu
   - OR open Command Prompt and type: `psql --version`

#### Create Database and User

**Option A: Using pgAdmin (GUI)**

1. Open pgAdmin 4
2. Connect to PostgreSQL server (enter your postgres password)
3. Right-click "Databases" → "Create" → "Database"
   - Database: `news_db`
   - Owner: `postgres`
4. Right-click "Login/Group Roles" → "Create" → "Login/Group Role"
   - Name: `news_user`
   - Definition tab → Password: `secure_password_123`
   - Privileges tab → Check "Can login?"
5. Right-click `news_db` → "Properties" → "Security"
   - Add `news_user` with ALL privileges

**Option B: Using Command Line**

```cmd
:: Open Command Prompt or PowerShell

:: Connect to PostgreSQL
psql -U postgres

:: Run these commands in PostgreSQL prompt:
```

```sql
CREATE DATABASE news_db;
CREATE USER news_user WITH PASSWORD 'secure_password_123';
GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;
\c news_db
GRANT ALL ON SCHEMA public TO news_user;
\q
```

#### Test Your Connection

```cmd
:: In Command Prompt
psql -h localhost -U news_user -d news_db

:: Enter password when prompted
:: Run a test query:
SELECT current_database();

:: Exit
\q
```

---

### Linux Installation (Ubuntu/Debian)

#### Install PostgreSQL

```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start and enable service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Verify it's running
sudo systemctl status postgresql
```

#### Create Database and User

```bash
# Switch to postgres user
sudo -u postgres psql

# Inside PostgreSQL prompt, run:
```

```sql
CREATE DATABASE news_db;
CREATE USER news_user WITH PASSWORD 'secure_password_123';
GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;
\c news_db
GRANT ALL ON SCHEMA public TO news_user;
\q
```

#### Configure PostgreSQL for Local Connections

```bash
# Edit pg_hba.conf to allow password authentication
sudo nano /etc/postgresql/15/main/pg_hba.conf

# Find the line that says:
# local   all             all                                     peer

# Change 'peer' to 'md5' for password authentication:
# local   all             all                                     md5

# Save and exit (Ctrl+X, then Y, then Enter)

# Restart PostgreSQL
sudo systemctl restart postgresql
```

#### Test Your Connection

```bash
# Connect with the new user
psql -h localhost -U news_user -d news_db

# Enter password when prompted
# Run a test query
SELECT current_database();

# Exit
\q
```

---

## Option 2: Cloud PostgreSQL (Easiest - No Installation)

### Supabase (Free Tier)

**Perfect for learning - 500MB free database**

1. **Sign Up:**
   - Visit: https://supabase.com/
   - Create account (free)

2. **Create Project:**
   - Click "New Project"
   - Choose organization
   - Project name: `news-pipeline`
   - Database password: (create a strong password)
   - Region: Choose closest to you
   - Click "Create new project"

3. **Get Connection Details:**
   - Go to Settings → Database
   - Find "Connection string" section
   - Use "Connection pooling" for better performance

4. **Connection Information:**
   ```
   Host: db.xxxxxxxxxxxxx.supabase.co
   Port: 5432
   Database: postgres
   User: postgres
   Password: (your project password)
   ```

5. **Create Database (Optional):**
   ```sql
   -- Connect using the Supabase SQL Editor or psql
   -- You can use the default 'postgres' database
   -- OR create a dedicated one:
   CREATE DATABASE news_db;
   ```

✅ **Advantage:** No installation needed, accessible from anywhere, free tier sufficient for learning

### ElephantSQL (Free Tier)

1. Sign up at https://www.elephantsql.com/
2. Create a "Tiny Turtle" free instance
3. Note your connection details
4. Use provided credentials in your `.env` file

### Other Cloud Providers

- **AWS RDS** - Free tier for 12 months
- **Google Cloud SQL** - $300 free credits
- **Heroku Postgres** - Free tier available
- **DigitalOcean Managed Databases** - Starting at $15/month

---

## Database Configuration for the Pipeline

### Understanding the Tables

The pipeline creates tables automatically on first run:

**For 8_guide.ipynb (Tesla news):**
```sql
CREATE TABLE news_articles (
    id BIGSERIAL PRIMARY KEY,
    source TEXT,
    title TEXT,
    short_summary TEXT,
    publish_date TIMESTAMPTZ,
    sentiment NUMERIC,
    short_date DATE,
    publish_est TIMESTAMPTZ,
    publish_pst TIMESTAMPTZ,
    publish_gmt TIMESTAMPTZ,
    topic TEXT,
    region TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**For 8_lab.ipynb (Disney news):**
```sql
CREATE TABLE disney_news_articles (
    -- All fields from above, PLUS:
    business_line TEXT  -- Parks, Movies, Streaming/Disney+, etc.
);
```

### Manual Table Creation (Optional)

If you want to create the table manually before running the pipeline:

```bash
# Connect to your database
psql -h localhost -U news_user -d news_db

# Paste the CREATE TABLE statement from above
# Then exit
\q
```

**Note:** The pipeline is designed to create the table automatically, so this step is optional.

---

## Connection Testing

### Test with psql Command Line

```bash
# Basic connection test
psql -h localhost -U news_user -d news_db -c "SELECT version();"

# Should output PostgreSQL version info
```

### Test with Python

Create a test file `test_postgres.py`:

```python
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Attempt connection
    conn = psycopg.connect(
        host=os.getenv('PGHOST', 'localhost'),
        port=os.getenv('PGPORT', '5432'),
        dbname=os.getenv('PGDATABASE', 'news_db'),
        user=os.getenv('PGUSER', 'news_user'),
        password=os.getenv('PGPASSWORD')
    )
    
    # Run test query
    with conn.cursor() as cur:
        cur.execute("SELECT current_database(), current_user, version();")
        result = cur.fetchone()
        print("✅ PostgreSQL Connection Successful!")
        print(f"   Database: {result[0]}")
        print(f"   User: {result[1]}")
        print(f"   Version: {result[2][:50]}...")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Connection Failed: {e}")
    print("\nTroubleshooting tips:")
    print("1. Verify PostgreSQL is running")
    print("2. Check your .env file has correct credentials")
    print("3. Ensure the database 'news_db' exists")
    print("4. Verify user 'news_user' has access privileges")
```

Run the test:
```bash
python test_postgres.py
```

---

## Environment Variables Reference

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `NEWS_API_KEY` | Your NewsAPI key | `abc123def456` |
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-proj-xyz...` |
| `PGHOST` | PostgreSQL host | `localhost` |
| `PGPORT` | PostgreSQL port | `5432` |
| `PGDATABASE` | Database name | `news_db` |
| `PGUSER` | Database user | `news_user` |
| `PGPASSWORD` | Database password | `secure_password_123` |

### Where to Set Variables

**For Notebooks (8_guide.ipynb, 8_lab.ipynb):**
```bash
# Create .env in the notebooks directory
cd ch08/notebooks/
cat > .env << EOF
NEWS_API_KEY=your_newsapi_key
OPENAI_API_KEY=sk-your-openai-key
PGHOST=localhost
PGPORT=5432
PGDATABASE=news_db
PGUSER=news_user
PGPASSWORD=your_password
EOF
```

**For Listings (8_1.py, 8_2.py, etc.):**
```bash
# Create .env in the ch08 root directory
cd ch08/
cat > .env << EOF
NEWS_API_KEY=your_newsapi_key
OPENAI_API_KEY=sk-your-openai-key
PGHOST=localhost
PGPORT=5432
PGDATABASE=news_db
PGUSER=news_user
PGPASSWORD=your_password
EOF
```

**For Airflow:**
- Use `airflow_project/.env` (separate from notebooks)
- May need `PGHOST=host.docker.internal` for Docker networking

---

## Common PostgreSQL Issues and Solutions

### Issue 1: "psql: command not found"

**Problem:** PostgreSQL client not in PATH

**Solution (macOS):**
```bash
# Add to your ~/.zshrc or ~/.bash_profile:
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"

# Reload shell
source ~/.zshrc
```

**Solution (Windows):**
- Add PostgreSQL bin directory to PATH environment variable
- Usually: `C:\Program Files\PostgreSQL\15\bin`

### Issue 2: "password authentication failed"

**Problem:** Incorrect password or user doesn't exist

**Solutions:**
```bash
# Reset password
sudo -u postgres psql -c "ALTER USER news_user WITH PASSWORD 'new_password';"

# Verify user exists
psql postgres -c "\du"

# Check connection parameters
psql -h localhost -U news_user -d news_db
```

### Issue 3: "could not connect to server"

**Problem:** PostgreSQL service not running

**Solutions:**
```bash
# macOS
brew services start postgresql@15

# Linux
sudo systemctl start postgresql

# Windows
# Use Services app or pgAdmin to start service
```

### Issue 4: "database 'news_db' does not exist"

**Problem:** Database wasn't created

**Solution:**
```bash
# Create the database
psql postgres -c "CREATE DATABASE news_db;"

# Verify it exists
psql postgres -c "\l" | grep news_db
```

### Issue 5: "permission denied for schema public"

**Problem:** User lacks schema privileges (PostgreSQL 15+)

**Solution:**
```bash
psql -U postgres -d news_db -c "GRANT ALL ON SCHEMA public TO news_user;"
```

### Issue 6: "role 'news_user' does not exist"

**Problem:** User wasn't created

**Solution:**
```bash
psql postgres -c "CREATE USER news_user WITH PASSWORD 'your_password';"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;"
```

---

## Advanced Configuration

### Connection Pooling (Optional)

For better performance with multiple connections:

```python
# Using connection pool
from psycopg_pool import ConnectionPool

pool = ConnectionPool(
    "postgresql://news_user:password@localhost:5432/news_db",
    min_size=1,
    max_size=10
)

# Get connection from pool
with pool.connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM news_articles LIMIT 10;")
```

### SSL Connections (For Cloud Databases)

```python
import psycopg

# For cloud providers requiring SSL
conn = psycopg.connect(
    host="your-cloud-host.com",
    port=5432,
    dbname="news_db",
    user="news_user",
    password="password",
    sslmode="require"  # or "verify-full" for strict verification
)
```

### Read-Only User (Optional)

For querying without write permissions:

```sql
-- Create read-only user
CREATE USER news_reader WITH PASSWORD 'readonly_password';
GRANT CONNECT ON DATABASE news_db TO news_reader;
GRANT USAGE ON SCHEMA public TO news_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO news_reader;
```

---

## Data Management

### Viewing Your Data

```sql
-- Connect to database
psql -h localhost -U news_user -d news_db

-- Count total articles
SELECT COUNT(*) FROM news_articles;

-- View latest articles
SELECT id, source, title, topic, sentiment, created_at
FROM news_articles
ORDER BY created_at DESC
LIMIT 10;

-- Check by topic
SELECT topic, COUNT(*) as count
FROM news_articles
GROUP BY topic
ORDER BY count DESC;

-- Check by region
SELECT region, COUNT(*) as count
FROM news_articles
GROUP BY region
ORDER BY count DESC;

-- Articles with negative sentiment
SELECT source, title, sentiment
FROM news_articles
WHERE sentiment < -0.3
ORDER BY sentiment ASC;
```

### For Disney Lab (business_line analysis)

```sql
-- View business line distribution
SELECT business_line, COUNT(*) as article_count,
       ROUND(AVG(sentiment)::numeric, 2) as avg_sentiment
FROM disney_news_articles
GROUP BY business_line
ORDER BY article_count DESC;

-- Top 5 most positive Parks articles
SELECT title, sentiment
FROM disney_news_articles
WHERE business_line = 'Parks'
ORDER BY sentiment DESC
LIMIT 5;
```

### Cleaning Up Data

```sql
-- Delete all articles (careful!)
DELETE FROM news_articles;

-- Delete articles older than 30 days
DELETE FROM news_articles
WHERE created_at < NOW() - INTERVAL '30 days';

-- Drop table completely
DROP TABLE IF EXISTS news_articles;

-- Recreate (will happen automatically on next pipeline run)
```

---

## Database Backup and Restore

### Backup Your Data

```bash
# Backup entire database
pg_dump -h localhost -U news_user -d news_db > news_db_backup.sql

# Backup just the news_articles table
pg_dump -h localhost -U news_user -d news_db -t news_articles > news_articles_backup.sql

# Compressed backup
pg_dump -h localhost -U news_user -d news_db | gzip > news_db_backup.sql.gz
```

### Restore from Backup

```bash
# Restore database
psql -h localhost -U news_user -d news_db < news_db_backup.sql

# Restore from compressed backup
gunzip -c news_db_backup.sql.gz | psql -h localhost -U news_user -d news_db
```

---

## Security Best Practices

### 1. Use Strong Passwords

```bash
# Generate a secure random password
openssl rand -base64 32

# Use this as your PGPASSWORD
```

### 2. Never Commit .env Files

```bash
# Ensure .env is in .gitignore
echo ".env" >> .gitignore
echo "*.env" >> .gitignore
```

### 3. Limit User Permissions

```sql
-- Don't grant SUPERUSER unless necessary
-- Use specific privileges:
GRANT SELECT, INSERT, UPDATE, DELETE ON news_articles TO news_user;
```

### 4. Use SSL for Cloud Connections

Always use `sslmode=require` when connecting to cloud databases.

---

## Docker PostgreSQL Alternative

If you prefer using Docker instead of local installation:

```bash
# Run PostgreSQL in Docker
docker run --name postgres-news \
  -e POSTGRES_USER=news_user \
  -e POSTGRES_PASSWORD=secure_password_123 \
  -e POSTGRES_DB=news_db \
  -p 5432:5432 \
  -d postgres:15

# Connect
psql -h localhost -U news_user -d news_db

# Stop container
docker stop postgres-news

# Start container
docker start postgres-news

# Remove container
docker rm -f postgres-news
```

**Advantage:** Clean isolation, easy cleanup  
**Disadvantage:** Need Docker running, data lost when container removed (unless using volumes)

---

## Verification Checklist

Before proceeding to the notebooks, verify:

- [ ] PostgreSQL is installed and running
- [ ] Database `news_db` exists
- [ ] User `news_user` exists with password
- [ ] You can connect: `psql -h localhost -U news_user -d news_db`
- [ ] User has privileges: Can run `SELECT 1;` successfully
- [ ] Schema privileges granted (PostgreSQL 15+)
- [ ] `.env` file created with correct credentials
- [ ] Python can connect (run `verify_setup.py` from ch08 root)

---

## Next Steps

Once PostgreSQL is set up:

1. ✅ **Configure environment variables** - See `sample.env` in this directory
2. ✅ **Run verification script** - `python verify_setup.py` from ch08 root
3. ✅ **Start notebooks** - Open `notebooks/8_guide.ipynb` or `notebooks/8_lab.ipynb`
4. ✅ **Run listings** - Try `python listing/8_1.py` to test extraction

---

## Getting Help

### If Connection Fails

1. **Verify service is running:**
   ```bash
   # macOS
   brew services list | grep postgresql
   
   # Linux
   sudo systemctl status postgresql
   ```

2. **Check PostgreSQL logs:**
   ```bash
   # macOS
   tail -f /opt/homebrew/var/log/postgresql@15.log
   
   # Linux
   sudo tail -f /var/log/postgresql/postgresql-15-main.log
   ```

3. **Test with superuser:**
   ```bash
   psql postgres  # Connect as default admin user
   \du            # List all users
   \l             # List all databases
   ```

4. **Verify network access:**
   ```bash
   # Check if PostgreSQL is listening
   netstat -an | grep 5432
   # OR
   lsof -i :5432
   ```

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `psql: command not found` | PostgreSQL not in PATH | Add to PATH or use full path |
| `FATAL: password authentication failed` | Wrong password | Reset password with ALTER USER |
| `FATAL: database "news_db" does not exist` | Database not created | Run CREATE DATABASE |
| `could not connect to server` | Service not running | Start PostgreSQL service |
| `permission denied for schema public` | Missing schema privileges | GRANT ALL ON SCHEMA public |

---

## Additional Resources

- **PostgreSQL Tutorial**: https://www.postgresqltutorial.com/
- **psql Command Reference**: https://www.postgresql.org/docs/current/app-psql.html
- **psycopg3 Documentation**: https://www.psycopg.org/psycopg3/docs/
- **Connection Troubleshooting**: https://wiki.postgresql.org/wiki/Troubleshooting_Connection_Problems

---

**Ready to proceed?** Once PostgreSQL is set up and tested, move on to configuring your API keys in the `.env` file!

