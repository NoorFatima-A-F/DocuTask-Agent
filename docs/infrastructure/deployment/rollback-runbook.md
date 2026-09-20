# Automated Rollback & Incident Recovery Runbook

## 1. Rollback Triggers
- **Automated Anomaly Tripping**: Elevated error rates (> 1%) or p99 latency degradation detected by Phase 9E observability.
- **Health Check Failure**: Endpoint health probes fail during progressive rollout.
- **AI Quality Drop**: Hallucination or confidence score regression detected on shadow/canary traffic.
- **Manual SRE Override**: Operator issues emergency rollback via CLI or API.

## 2. Triggering Rollback Programmatically
```python
from app.infrastructure.deployment.sdk import DeploymentSDK
from app.infrastructure.deployment.rollback import RollbackTriggerType

sdk = DeploymentSDK()
rca_report = sdk.rollback(
    deployment_id="dep-12345",
    reason="Elevated 5xx error rate detected during 25% canary step",
    trigger_type=RollbackTriggerType.METRIC_ANOMALY
)

print(f"Restored version: {rca_report.restored_version}")
print(f"RCA Summary: {rca_report.root_cause_summary}")
```
