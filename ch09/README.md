# Chapter 9: Advanced Data Pipeline Orchestration

This chapter builds on the multi-agent architecture from Chapter 8 and explores advanced data pipeline orchestration, scheduling, monitoring, and production deployment strategies using Apache Airflow.

## Chapter Overview

Chapter 9 focuses on taking data pipelines to production by addressing:

1. **Advanced Orchestration** - Complex dependencies and conditional workflows
2. **Scheduling & Automation** - Time-based and event-driven triggers
3. **Monitoring & Alerting** - Pipeline health and performance tracking
4. **Error Handling & Recovery** - Robust retry strategies and failure management
5. **Production Best Practices** - Scalability, security, and maintenance
6. **Multi-Environment Deployment** - Dev, staging, and production workflows

The chapter uses real-world scenarios to demonstrate production-ready data engineering.

## Quick Start

**New to this chapter?** Follow these steps to get started quickly:

1. **Install dependencies**: 
   ```bash
   cd ch09/
   pip install -r requirements.txt
   ```
2. **Configure API keys**: 
   ```bash
   cp sample.env .env
   # Edit .env with your actual API keys
   ```
3. **Launch Jupyter**: 
   ```bash
   cd notebooks/
   jupyter lab
   # Open 9_guide_test.ipynb (10 rows) or 9_guide_full.ipynb (all rows)
   ```
4. **Optional - Start Airflow**: 
   ```bash
   cd airflow_project/
   ./quickstart.sh
   # Access at http://localhost:8080 (login: airflow / airflow)
   ```

For detailed setup instructions, see the [Complete Setup Instructions](#complete-setup-instructions) section below.

## Directory Structure

```
ch09/
├── README.md                    # This file
├── notebooks/
│   ├── 9_guide_test.ipynb      # Chapter walkthrough (10 rows - fast testing)
│   ├── 9_guide_full.ipynb      # Chapter walkthrough (all 729 rows - full analysis)
│   └── 9_lab.ipynb             # Hands-on lab exercises
├── listings/                    # Individual code examples
│   └── (code examples to be added)
├── data/                        # CSV files and data resources
├── airflow_project/             # Complete Airflow orchestration
│   ├── dags/
│   │   └── (DAG files to be added)
│   ├── docker-compose.yaml      # Airflow Docker configuration
│   ├── quickstart.sh            # Quick start script
│   ├── README.md                # Airflow project overview
│   ├── GETTING_STARTED.md       # Beginner's guide to Airflow
│   ├── SETUP_GUIDE.md           # Complete setup documentation
│   └── START_HERE.md            # Quick reference
├── images/                      # Chapter figures
├── setup/                       # Setup files and resources
├── requirements.txt             # Python dependencies
└── sample.env                   # Environment variables template
```

## Prerequisites

### Technical Prerequisites
- **Python 3.8+** - Required for all exercises and code examples
- **Completion of Chapter 8** - Multi-agent architectures are foundational
- **PostgreSQL database** - For data loading exercises (local or cloud)
- **Docker Desktop** - Required for Airflow orchestration
- **Command line/terminal usage** - For running scripts and managing services
- **Basic SQL knowledge** - For database queries and operations

### Knowledge Prerequisites
- **Multi-agent systems** - Understanding specialized agent collaboration
- **ETL pipeline concepts** - Extraction, transformation, loading workflows
- **Workflow orchestration** - Task dependencies and scheduling
- **Error handling patterns** - Retry logic and failure recovery
- **Docker basics** - Container concepts and docker-compose

### Account Requirements
- **NewsAPI Account** - Required for data extraction
  - Sign up at: https://newsapi.org/
  - Free tier available (100 requests/day)
  
- **OpenAI API Account** - Required for AI processing
  - Sign up at: https://platform.openai.com/
  - Requires valid payment method
  - Estimated cost for chapter exercises: $5-10 USD
  
- **PostgreSQL Database** - Required for data storage
  - Local installation OR cloud provider
  - Free tier available from multiple providers

## Complete Setup Instructions

### Step 1: Environment Preparation

#### Option A: Using Virtual Environment (Recommended)
```bash
# Navigate to the chapter directory
cd ch09/

# Create a new virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Verify Python version (should be 3.8+)
python --version
```

#### Option B: Using Conda
```bash
# Create a new conda environment
conda create -n ch09_data_ai python=3.10

# Activate the environment
conda activate ch09_data_ai

# Navigate to the chapter directory
cd ch09/
```

### Step 2: Install Dependencies

```bash
# Make sure you're in the ch09 directory
cd ch09/

# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(pandas|openai|pydantic|psycopg|matplotlib|seaborn)"
```

**Important**: After installation, if using Jupyter, restart your kernel to ensure packages are loaded.

### Step 3: API Keys Configuration

```bash
# Create .env file from template
cp sample.env .env

# Edit with your actual keys
nano .env  # or use your preferred editor
```

Update the `.env` file with your actual API keys:
```env
NEWS_API_KEY=your_actual_newsapi_key_here
OPENAI_API_KEY=sk-your-actual-openai-key-here
PGHOST=localhost
PGPORT=5432
PGDATABASE=news_db
PGUSER=news_user
PGPASSWORD=your_secure_password
```

### Step 4: PostgreSQL Database Setup

#### Option A: Local PostgreSQL Installation

**macOS (using Homebrew):**
```bash
# Install PostgreSQL
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14

# Create database and user
psql postgres -c "CREATE DATABASE news_db;"
psql postgres -c "CREATE USER news_user WITH PASSWORD 'your_secure_password';"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;"
```

**Ubuntu/Debian:**
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql -c "CREATE DATABASE news_db;"
sudo -u postgres psql -c "CREATE USER news_user WITH PASSWORD 'your_secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;"
```

#### Option B: Cloud PostgreSQL

Use any cloud provider:
- Supabase (free tier)
- AWS RDS
- Google Cloud SQL
- Azure Database for PostgreSQL

### Step 5: Start Airflow

```bash
# Navigate to Airflow project
cd airflow_project/

# Configure environment
cp env.template .env
# Edit .env with your keys and database credentials

# Start Airflow
./quickstart.sh

# Access UI
open http://localhost:8080
# Username: airflow
# Password: airflow
```

## Key Learning Objectives

By the end of this chapter, you will:

- Design production-ready data pipelines with complex dependencies
- Implement advanced scheduling strategies (time-based, event-driven)
- Build robust error handling and retry mechanisms
- Monitor pipeline health and performance metrics
- Deploy pipelines across multiple environments
- Implement security best practices for production
- Scale pipelines for high-volume data processing
- Debug and troubleshoot production pipeline issues

## Airflow Project

The `airflow_project/` directory contains the complete orchestration setup.

### Quick Start

```bash
cd airflow_project/

# Start Airflow
./quickstart.sh

# Access UI at http://localhost:8080
```

### Documentation

- **START_HERE.md** - Quick reference
- **GETTING_STARTED.md** - Beginner's guide  
- **SETUP_GUIDE.md** - Complete setup and troubleshooting
- **README.md** - Project overview

### Features

- Automated workflow orchestration
- Task dependency management
- Error handling and retries
- Monitoring and logging
- Configurable scheduling
- Production-ready setup

## Key Concepts

### Production Orchestration
- Task dependencies and parallelization
- Dynamic DAG generation
- Conditional workflow execution
- Cross-DAG dependencies

### Monitoring & Observability
- Pipeline health metrics
- Performance tracking
- Error rate monitoring
- Cost tracking and optimization

### Error Handling
- Retry strategies with exponential backoff
- Failure notifications
- Partial failure recovery
- Data quality validation

### Deployment Strategies
- Environment-specific configurations
- Blue-green deployments
- Canary releases
- Rollback procedures

## Common Commands

```bash
# Start Airflow
cd airflow_project/
./quickstart.sh

# Stop Airflow
docker compose down

# View logs
docker compose logs -f

# Restart
docker compose restart

# Trigger DAG
docker exec -it <container> airflow dags trigger dag_name

# List DAGs
docker exec -it <container> airflow dags list
```

## Troubleshooting

### Airflow not starting
```bash
# Check Docker is running
docker ps

# View logs for errors
docker compose logs

# Restart fresh
docker compose down -v
./quickstart.sh
```

### Database connection issues
```bash
# Try alternative host
PGHOST=host.docker.internal

# Verify PostgreSQL is running
psql -h localhost -U news_user -d news_db
```

### DAG not appearing
- Wait 30-60 seconds and refresh
- Check for syntax errors in DAG file
- Verify file is in dags/ directory
- Check logs: `docker compose logs | grep -i error`

## Cost Management

### OpenAI API
- Estimated cost for exercises: $5-10 USD
- Set usage limits in OpenAI dashboard
- Use gpt-4o-mini for testing
- Cache results when possible

### NewsAPI
- Free tier: 100 requests/day
- Plan queries to stay within limits
- Consider upgrading for production

## Best Practices

1. **Version Control** - Track all pipeline code in git
2. **Environment Variables** - Never hardcode credentials
3. **Idempotent Operations** - Safe to rerun tasks
4. **Comprehensive Logging** - Track all pipeline actions
5. **Data Validation** - Verify quality at each stage
6. **Error Notifications** - Alert on failures
7. **Resource Monitoring** - Track CPU, memory, costs
8. **Documentation** - Document all workflows and decisions

## Lab Exercises

The lab section provides hands-on experience with:

1. **Complex DAG Design** - Multi-path conditional workflows
2. **Advanced Scheduling** - Time-based and event-driven triggers
3. **Error Recovery** - Implementing robust retry strategies
4. **Performance Optimization** - Parallelization and caching
5. **Monitoring Dashboard** - Pipeline health metrics
6. **Multi-Environment Deploy** - Dev, staging, production

## Additional Resources

### Documentation
- **Airflow Docs**: https://airflow.apache.org/docs/
- **Docker Docs**: https://docs.docker.com/
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **OpenAI Docs**: https://platform.openai.com/docs

### Related Chapters
- **Chapter 8** - Multi-agent architecture foundations
- **Chapter 7** - Advanced transformations
- **Chapter 6** - Data quality and validation

## Next Steps

After completing this chapter:

1. Build production pipelines for your use cases
2. Implement monitoring and alerting
3. Deploy to cloud infrastructure
4. Explore alternative orchestrators (Prefect, Dagster)
5. Add advanced features (streaming, real-time)
6. Optimize for cost and performance

## Getting Help

### Support Resources
- Check SETUP_GUIDE.md for detailed troubleshooting
- Review Airflow documentation
- View logs: `docker compose logs -f`
- Verify all prerequisites are met

### If Issues Persist
1. Ensure Docker Desktop is running
2. Verify PostgreSQL is accessible
3. Check API keys are correct
4. Review error messages in logs
5. Try clean restart: `docker compose down -v && ./quickstart.sh`

---

**Ready to begin?** Start with `airflow_project/START_HERE.md` for quick setup, or explore the notebooks for detailed walkthroughs!

