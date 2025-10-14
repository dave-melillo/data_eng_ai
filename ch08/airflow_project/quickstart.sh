#!/bin/bash

# Airflow News Pipeline - Quick Start
# Simple single-container setup that actually works!

set -e

echo "=========================================="
echo "  Airflow News Pipeline - Quick Start"
echo "=========================================="
echo ""

if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker not running. Start Docker Desktop first!"
    exit 1
fi
echo "✅ Docker is running"

if [ ! -f .env ]; then
    cp env.template .env
    echo "✅ Created .env file"
    echo ""
    echo "🔧 IMPORTANT: Edit .env with your API keys:"
    echo "   - NEWS_API_KEY=your_key_here"
    echo "   - OPENAI_API_KEY=sk-proj-your_key_here"
    echo "   - PGPASSWORD=your_db_password"
    echo ""
    echo "Then run this script again: ./quickstart.sh"
    exit 0
fi
echo "✅ .env file found"

mkdir -p airflow-data logs dags plugins config
chmod -R 777 airflow-data logs 2>/dev/null || true

echo ""
echo "🚀 Starting Airflow..."
echo "   First run: 2-3 minutes (downloads image, installs packages)"
echo "   Subsequent runs: 30-60 seconds"
echo ""

docker compose up -d

echo ""
echo "⏳ Waiting for Airflow to start (60-90 seconds)..."
sleep 20

COUNTER=0
while [ $COUNTER -lt 40 ]; do
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "✅ Airflow is ready!"
        break
    fi
    if [ $((COUNTER % 10)) -eq 0 ]; then
        echo "   Still starting... ($COUNTER/40)"
    fi
    sleep 2
    COUNTER=$((COUNTER+1))
done

echo ""
echo "=========================================="
echo "  ✅ Airflow is Running!"
echo "=========================================="
echo ""
echo "🌐 http://localhost:8080"
echo "   Username: airflow"
echo "   Password: airflow"
echo ""
echo "📋 To run the pipeline:"
echo "   1. Open http://localhost:8080"
echo "   2. Login with airflow/airflow"
echo "   3. Find 'news_articles_pipeline' DAG"
echo "   4. Toggle it ON (if paused)"
echo "   5. Click ▶️ → 'Trigger DAG w/ config'"
echo "   6. Enter:"
echo '      {"query": "Tesla", "from_date": "2025-10-05", "to_date": "2025-10-08"}'
echo ""
echo "🛠️  Useful commands:"
echo "   View logs:  docker compose logs -f"
echo "   Stop:       docker compose down"
echo "   Restart:    docker compose restart"
echo ""
echo "📚 For detailed docs, see SETUP_GUIDE.md"
echo ""
