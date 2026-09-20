# Operational Runbook: Celery Worker Crash & Processing Node Recovery

## 1. Problem Description
One or more Celery worker nodes have crashed, missed heartbeats for $>15$ seconds, or suffered an OOM SIGKILL while processing large, complex documents.

## 2. Detection
- **Alert**: Celery heartbeat monitor detects worker offline (`worker_missed_heartbeat`).
- **Health Check**: `worker_health` returns `DEGRADED` in `production_health_report.json`.
- **Logs**: `WorkerLostError: Worker exited prematurely: exitcode 137 (SIGKILL)`.

## 3. Impact
- Documents currently assigned to the terminated worker stall in processing.
- Queue consumption throughput decreases proportionally to lost worker concurrency.
- Severity: **SEV2** (if multiple workers fail) or **SEV3** (if single worker auto-heals).

## 4. Diagnosis
1. Inspect running Celery worker containers:
   ```bash
   docker ps -f "name=docutask-worker"
   ```
2. Check kernel OOM kill events in container logs:
   ```bash
   docker logs --tail 100 docutask-worker-1 | grep -i "oom\|killed\|sigkill"
   ```
3. Verify unacknowledged task counts in Redis:
   ```bash
   docker exec -it docutask-redis redis-cli hlen unacked
   ```

## 5. Resolution & Remediation
1. Trigger automated worker restart and health validation:
   ```bash
   docker restart docutask-worker-1
   ```
2. Re-queue orphan unacknowledged tasks into the active Redis queue:
   ```bash
   docker exec -it docutask-api python -c "from app.workers.celery_app import celery_app; celery_app.control.purge()"
   ```
3. If memory pressure persists, increase container memory reservation:
   ```bash
   docker update --memory 2048m --memory-swap 2048m docutask-worker-1
   ```

## 6. Validation
- Verify worker registration with Celery master:
  ```bash
  docker exec -it docutask-api celery -A app.workers.celery_app inspect ping
  ```
- Confirm all 8 worker replicas respond with `pong` and task processing resumes normally.
