# Scheduler SRE Operational Runbook

## Common Operational Procedures

### 1. Draining a Worker for Maintenance
```bash
curl -X POST http://localhost:8000/api/v1/infrastructure/workers/wrk-ocr-01/drain \
  -H "Content-Type: application/json" \
  -d '{"reason": "Host maintenance"}'
```

### 2. Triggering Lost Worker Recovery Loop
```bash
curl -X POST http://localhost:8000/api/v1/infrastructure/scheduling/recover
```

### 3. Cancelling a Runaway Workload
```bash
curl -X POST http://localhost:8000/api/v1/infrastructure/scheduling/workloads/wkl-1234/cancel
```
