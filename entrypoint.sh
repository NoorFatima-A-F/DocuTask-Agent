#!/bin/bash
set -e

# Run Redis daemonized using /tmp to prevent permission issues for non-root users
redis-server --daemonize yes --dir /tmp

# Start Celery worker in the background (concurrency 1 to conserve free-tier memory)
celery -A app.jobs.worker worker --concurrency=1 --loglevel=info &

# Start FastAPI via Uvicorn on Hugging Face default port 7860
exec uvicorn app.main:app --host 0.0.0.0 --port 7860
