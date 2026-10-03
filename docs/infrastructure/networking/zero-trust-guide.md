# Zero-Trust Security & Identity Verification Guide

## 1. Principles
- **Never Trust, Always Verify**: Every service-to-service call is untrusted until caller identity, destination identity, mTLS certificate, and authorization policies are validated.
- **Least Privilege**: Workloads are granted minimal required access to specific paths, HTTP methods, and tenant data.
- **Continuous Verification**: Identity and permissions are evaluated on every single request, not just at session establishment.

## 2. SPIFFE Identity Standard
Format: `spiffe://{trust_domain}/ns/{namespace}/sa/{service_account}`

```python
from app.infrastructure.networking.security import WorkloadIdentityManager

id_mgr = WorkloadIdentityManager(trust_domain="docutask.internal")
identity = id_mgr.create_identity(namespace="prod-workers", service_account="ocr-processor")
svid = id_mgr.issue_svid(identity, ttl_seconds=3600)
```

## 3. Zero-Trust Policy Engine
```python
from app.infrastructure.networking.security import ZeroTrustPolicyEngine, ZeroTrustRule
from app.infrastructure.networking.control_plane import ZeroTrustAction

engine = ZeroTrustPolicyEngine()
engine.add_rule(ZeroTrustRule(
    rule_id="rule-worker-access",
    name="Allow Workflow Coordinator to OCR Worker",
    action=ZeroTrustAction.ALLOW,
    source_spiffe_pattern="spiffe://docutask.internal/ns/workflows/sa/coordinator",
    target_spiffe_pattern="spiffe://docutask.internal/ns/workers/sa/ocr-processor",
    allowed_methods=["POST"],
    allowed_paths=["/v1/ocr/*"],
    tenant_scope=["*"],
))
```
