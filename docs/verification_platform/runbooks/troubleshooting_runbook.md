# Verification Platform Troubleshooting Runbook

## Diagnostic Flowchart
1. **Audit Chain Broken Alert**:
   - Check `app/contexts/audit/` logs.
   - Run `verify_chain_integrity()` to locate the tampered record index.
2. **Quality Gate Failure Blocker**:
   - Inspect metric outputs in `app/contexts/metrics/`.
   - Check if threshold breach was caused by upstream data drift or prompt regression.
3. **Environment Readiness Probe Timeout**:
   - Check host dependency health and resource quotas.
