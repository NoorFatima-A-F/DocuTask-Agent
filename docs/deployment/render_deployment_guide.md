# Live Deployment Guide (Render / Railway / AWS)

Deploying a live instance gives technical reviewers, recruiters, and clients an interactive Swagger UI to test document extraction with zero local setup.

---

## 1. Deploying to Render (Blueprint / 1-Click)

DocuTask Agent includes a production `render.yaml` Blueprint manifest that automatically provisions:
1. **`docutask-api`**: FastAPI web service running Uvicorn.
2. **`docutask-worker`**: Celery asynchronous extraction worker.
3. **`docutask-redis`**: Managed Redis instance for the task broker and idempotency cache.

### Step-by-Step Instructions:
1. Fork or push `NoorFatima-A-F/DocuTask-Agent` to your GitHub account.
2. Log in to [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** $\rightarrow$ **Blueprint**.
4. Connect your `DocuTask-Agent` repository.
5. Render will detect `render.yaml` and configure the 3 services automatically.
6. Under Environment Variables for `docutask-api` and `docutask-worker`, supply:
   - `GEMINI_API_KEY`: Your Google Gemini API Key from Google AI Studio.
7. Click **Apply**.
8. Once built, open your live URL: `https://docutask-api.onrender.com/docs` to test interactive document processing!

---

## 2. Deploying to Railway

1. Open [Railway.app](https://railway.app/).
2. Click **New Project** $\rightarrow$ **Deploy from GitHub repo**.
3. Add a **Redis** service from Railway's template catalog.
4. Set the following environment variables on the web service:
   - `REDIS_URL`: `${{Redis.REDIS_URL}}`
   - `GEMINI_API_KEY`: `<your_gemini_api_key>`
   - `SECRET_KEY`: `<random_32_character_hex_string>`
5. Deploy and access interactive documentation at `https://<your-app>.up.railway.app/docs`.

---

## 3. Deploying via Docker Compose (Local & Self-Hosted VPS)

```bash
# Clone and enter repository
git clone https://github.com/NoorFatima-A-F/DocuTask-Agent.git
cd DocuTask-Agent

# Configure environment
cp .env.example .env

# Build and start services in background
docker compose up -d --build

# Inspect running containers
docker compose ps

# Access local Swagger docs
open http://localhost:8000/docs
```
