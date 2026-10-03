# Webhooks & Event Subscriptions Guide

DocuTask Governance dispatches real-time HTTPS webhooks for compliance events, policy violations, and approval interventions.

---

## Supported Events
* `GovernanceDecisionCreated`: Emitted whenever an evaluation occurs.
* `PolicyViolation`: Emitted when an action is blocked or flagged.
* `ApprovalRequired`: Emitted when human oversight is triggered.
* `RiskDetected`: Emitted on high/critical risk anomaly.
* `AuditGenerated`: Emitted when immutable audit proof is generated.
* `ComplianceFailure`: Emitted when control validation fails.

---

## Verifying Webhook Signatures
Every webhook delivery contains header `X-Governance-Signature` with HMAC-SHA256 of the JSON body:

```python
import hmac
import hashlib

def verify_signature(payload_bytes: bytes, secret: str, header_sig: str) -> bool:
    mac = hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256)
    expected = f"sha256={mac.hexdigest()}"
    return hmac.compare_digest(expected, header_sig)
```
