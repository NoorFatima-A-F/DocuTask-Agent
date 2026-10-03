# Operational Runbook: Redis Task Queue Backlog & Overflow Remediation

## 1. Problem Description
The document processing task queue depth exceeds standard operational limits ($>500$ tasks) and demonstrates monotonic growth during high-volume burst ingestion.

## 2. Detection
- **Alert**: `ALT-QUEUE-003: Redis Queue Depth Monotonic Growth` ($>500$ tasks for $>3$ minutes).
- **Health Check**: `queue_health` reports backlog spike.
- **Metrics**: `redis_queue_length > 500`.

## 3. Impact
- End-to-end document processing turnaround latency degrades from $<2$ seconds to $>30$ seconds.
- Potential violation of P95 latency SLO targets.
- Severity: **SEV2** (Major).

## 4. Diagnosis
1. Inspect Redis queue length:
   ```bash
   docker exec -it docutask-redis redis-cli llen celery
   ```
2. Measure current consumption throughput vs. ingestion rate:
   ```bash
   curl -s http://localhost:8000/api/v1/operations/health | jq .subsystems
   ```
3. Check for stuck or hanging OCR / AI worker tasks:
   ```bash
   docker exec -it docutask-api celery -A app.workers.celery_app inspect active
   ```

## 5. Resolution & Remediation
1. Trigger automated horizontal elasticity to scale worker pool from 4 to 8 instances:
   ```bash
   docker compose up -d --scale worker=8
   ```
2. Enable client-side backpressure rate-limiting on bulk upload endpoints:
   ```bash
   curl -X POST http://localhost:8000/api/v1/operations/governance/rate-limit?tier=bulk&rps=10
   ```
3. Monitor queue drain rate until queue depth falls below 20 tasks.

## 6. Validation
- Verify queue depth normalizes:
  ```bash
  docker exec -it docutask-redis redis-cli llen celery
  ```
- Validate P95 document processing latency returns to $<500$ms.
