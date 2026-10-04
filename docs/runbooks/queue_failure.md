# Redis Queue Broker & Sentinel Outage Runbook

**Runbook ID**: RB-003
**Target Component**: Redis Cluster & Queue Storage
**Automated CLI Command**: `agy runbook exec queue_failure --sentinel-failover`
**Review Cadence**: Monthly Verified

---

## 1. Detection
- **Prometheus Alert**: `Alert: RedisCluster&QueueStorageDegraded`
- **Threshold**: Heartbeat missing for > 15 seconds or HTTP 5xx rate > 2%.
- **Notification Channels**: `#incident-disaster-recovery`, PagerDuty Tier-1 SRE.

---

## 2. Impact
- **Service Affected**: Redis Cluster & Queue Storage
- **User Impact**: Potential delays in document processing; 0 data loss guaranteed via transactional storage.
- **SLA Bound**: RTO <= 15 min, RPO = 0s.

---

## 3. Diagnosis
1. Check component status:
   ```bash
   kubectl get pods -l app=queue -n docutask
   kubectl logs --tail=100 -l app=queue -n docutask
   ```
2. Verify network connectivity and health endpoints:
   ```bash
   curl -f http://localhost:8000/api/health/live
   ```

---

## 4. Recovery Steps

### Option A: Automated Recovery (Recommended)
Run the automated recovery CLI:
```bash
agy runbook exec queue_failure --sentinel-failover
```

### Option B: Manual Recovery Procedure
1. Drain traffic from failing node:
   ```bash
   kubectl cordon <node-name>
   ```
2. Trigger standby promotion / pod restart:
   ```bash
   kubectl rollout restart deployment/queue -n docutask
   ```
3. Verify new instance reaches Ready state.

---

## 5. Validation
- Run health validation probe:
  ```bash
  python -m pytest tests/platform_verification/test_enterprise_operational_resilience.py -k "queue"
  ```
- Confirm queue processing resumes and latency returns to baseline.

---

## 6. Rollback
If recovery fails or induces unintended side-effects:
```bash
agy runbook rollback --runbook-id RB-003 --restore-snapshot
```
