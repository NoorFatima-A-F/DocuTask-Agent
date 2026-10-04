# Operational Runbook: Production Deployment Rollout Failure & Canary Rollback

## 1. Problem Description
A newly deployed container version or database migration causes health check failures, error rate spikes ($>1\%$), or performance regression immediately post-release.

## 2. Detection
- **CI/CD Release Gate**: Stage 7 gatekeeper reports `BLOCKED` or deployment verification fails.
- **Canary Monitor**: Error rate on new container version exceeds 0.5%.
- **Logs**: Unhandled exceptions or schema mismatch errors.

## 3. Impact
- Users experience 500 Internal Server Errors or broken document workflow pipelines.
- Risk of exhausting monthly reliability error budget.
- Severity: **SEV1** (Critical) or **SEV2** (Major).

## 4. Diagnosis
1. Inspect container deployment status and recent restart counts:
   ```bash
   docker ps -a --filter "name=docutask"
   ```
2. Check recent application error stack traces:
   ```bash
   docker logs --tail 200 docutask-api | grep -i "error\|exception\|traceback"
   ```
3. Verify database schema migration version:
   ```bash
   docker exec -it docutask-api alembic current
   ```

## 5. Resolution & Remediation
1. Initiate automated rollback to last certified release digest:
   ```bash
   docker compose -f docker-compose.yml down
   docker compose -f docker-compose.previous.yml up -d
   ```
2. If database migration occurred, roll back migration:
   ```bash
   docker exec -it docutask-api alembic downgrade -1
   ```
3. Re-route production traffic to stable rollback containers and freeze new releases.

## 6. Validation
- Validate health endpoints return 200 OK:
  ```bash
  curl -s http://localhost:8000/health | jq .
  ```
- Confirm error rate drops back to $<0.05\%$.
