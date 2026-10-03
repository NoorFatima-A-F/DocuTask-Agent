# Release Management & Governance Approval Guide

## 1. Release Lifecycle States
`CREATED` -> `VALIDATED` -> `APPROVED` -> `RELEASED` -> `DEPLOYED` -> `MONITORED` -> `COMPLETED`.

## 2. Multi-Stakeholder Approval Requirements
Before a release can transition to `RELEASED` for production deployment, formal sign-offs are mandatory from:
- **Governance Lead**: Verifies compliance policies and regulatory criteria.
- **Security Officer**: Verifies vulnerability scans and cryptographic signatures.
- **SRE Lead**: Verifies error budget availability and current reliability state.

```python
from app.infrastructure.deployment.releases import ReleaseManager, ReleaseApprovalGate, ApprovalDecision

gate = ReleaseApprovalGate()
mgr = ReleaseManager(approval_gate=gate)

rel = mgr.create_release(
    version="2.0.0",
    components_changed=["ocr-service", "gateway"],
    artifact_ids=["art-1", "art-2"],
)

gate.record_decision(rel.release_id, "auditor-01", "governance", ApprovalDecision.APPROVED)
gate.record_decision(rel.release_id, "sec-officer", "security", ApprovalDecision.APPROVED)
gate.record_decision(rel.release_id, "sre-lead", "sre", ApprovalDecision.APPROVED)

mgr.transition_status(rel.release_id, ReleaseLifecycleStatus.RELEASED)
```
