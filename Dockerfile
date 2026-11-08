# syntax=docker/dockerfile:1

# ---- 1. Frontend build (Node 20) ---------------------------------------------
FROM node:20-bookworm-slim AS frontend
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

# ---- 2. Python wheels ----------------------------------------------------------
FROM python:3.12-slim-bookworm AS wheels
WORKDIR /build
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
 && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ---- 3. Runtime ----------------------------------------------------------------------
FROM python:3.12-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860 \
    STORAGE_LOCAL_DIR=/app/storage \
    STORAGE_LOCAL_PATH=/app/storage

# tesseract: OCR engine (the app refuses to report ready without it).
# redis-server: only used by ROLE=all-in-one (single-container hosting such as HF Spaces).
RUN apt-get update \
 && apt-get install -y --no-install-recommends tesseract-ocr tesseract-ocr-eng redis-server \
 && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 10001 app && useradd --uid 10001 --gid app --create-home --shell /usr/sbin/nologin app

WORKDIR /app
COPY --from=wheels /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* && rm -rf /wheels

COPY alembic.ini ./
COPY migrations/ ./migrations/
COPY app/ ./app/
COPY --from=frontend /frontend/dist ./frontend/dist
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod 0755 /usr/local/bin/entrypoint.sh && mkdir -p /app/storage && chown -R app:app /app/storage

USER app
EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import os,urllib.request; urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\",\"7860\")}/healthz', timeout=4)" || exit 1

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD []
