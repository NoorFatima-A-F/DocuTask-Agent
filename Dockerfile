# Multi-stage production Dockerfile for AI Document Processing Platform (Hugging Face Spaces)
FROM python:3.10-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final runtime stage
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860

# Install runtime dependencies: redis-server, tesseract-ocr, build essentials
RUN apt-get update && apt-get install -y --no-install-recommends \
    redis-server \
    tesseract-ocr \
    poppler-utils \
    libpq5 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY . /app

# Configure non-root user 1000 (Hugging Face Spaces default user) and runtime permissions
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/storage/uploads /tmp && \
    chmod +x /app/entrypoint.sh && \
    chown -R appuser:appuser /app /tmp

USER 1000

EXPOSE 7860

CMD ["/bin/bash", "./entrypoint.sh"]
