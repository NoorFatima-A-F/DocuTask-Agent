#!/bin/bash
# Single-container entrypoint (Hugging Face Spaces): local Redis + Celery worker + API.
set -e

# Redis daemonized in /tmp (non-root friendly); the API and worker share it.
redis-server --daemonize yes --dir /tmp
export REDIS_URL="${REDIS_URL:-redis://127.0.0.1:6379/0}"

# Celery worker in the background (concurrency 1 to conserve free-tier memory)
celery -A app.jobs.celery_app worker --concurrency=1 --loglevel=info &

# FastAPI on the Hugging Face default port 7860
exec uvicorn app.main:app --host 0.0.0.0 --port 7860
