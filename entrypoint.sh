#!/bin/sh
# Container entrypoint. Usage: entrypoint.sh [web|worker|all-in-one]  (or set ROLE)
#   web         run migrations, then serve the API + UI on $PORT (default 7860)
#   worker      run the Celery extraction worker
#   all-in-one  local Redis + worker + web in one container (e.g. Hugging Face Spaces)
set -eu

PORT="${PORT:-7860}"
role="${1:-${ROLE:-web}}"

migrate() {
  alembic upgrade head
}

case "$role" in
  web)
    migrate
    exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --proxy-headers --forwarded-allow-ips "${FORWARDED_ALLOW_IPS:-127.0.0.1}"
    ;;
  worker)
    exec celery -A app.jobs.celery_app worker --loglevel=info --concurrency="${WORKER_CONCURRENCY:-2}"
    ;;
  all-in-one)
    redis-server --daemonize yes --dir /tmp --save "" --appendonly no
    export REDIS_URL="${REDIS_URL:-redis://127.0.0.1:6379/0}"
    migrate
    celery -A app.jobs.celery_app worker --loglevel=info --concurrency="${WORKER_CONCURRENCY:-1}" &
    exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
    ;;
  *)
    exec "$@"
    ;;
esac
