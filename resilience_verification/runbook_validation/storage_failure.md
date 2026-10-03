# AWS S3 / MinIO Document Storage Failure Runbook

**Runbook ID**: RB-004
**Target Component**: Document Vault & Thumbnail Store
**Automated CLI Command**: `agy runbook exec storage_failure --switch-region us-west-2`
**Review Cadence**: Monthly Verified

---

## 1. Detection
- **Prometheus Alert**: `Alert: DocumentVault&ThumbnailStoreDegraded`
- **Threshold**: Heartbeat missing for > 15 seconds or HTTP 5xx rate > 2%.
- **Notification Channels**: `#incident-disaster-recovery`, PagerDuty Tier-1 SRE.

---

## 2. Impact
- **Service Affected**: Document Vault & Thumbnail Store
- **User Impact**: Potential delays in document processing; 0 data loss guaranteed via transactional storage.
- **SLA Bound**: RTO <= 15 min, RPO = 0s.

---

## 3. Diagnosis
1. Check component status:
   ```bash
   kubectl get pods -l app=storage -n docutask
   kubectl logs --tail=100 -l app=storage -n docutask
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
agy runbook exec storage_failure --switch-region us-west-2
```

### Option B: Manual Recovery Procedure
1. Drain traffic from failing node:
   ```bash
   kubectl cordon <node-name>
   ```
2. Trigger standby promotion / pod restart:
   ```bash
   kubectl rollout restart deployment/storage -n docutask
   ```
3. Verify new instance reaches Ready state.

---

## 5. Validation
- Run health validation probe:
  ```bash
  python -m pytest tests/platform_verification/test_enterprise_operational_resilience.py -k "storage"
  ```
- Confirm queue processing resumes and latency returns to baseline.

---

## 6. Rollback
If recovery fails or induces unintended side-effects:
```bash
agy runbook rollback --runbook-id RB-004 --restore-snapshot
```
