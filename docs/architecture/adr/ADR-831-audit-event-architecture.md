# ADR-831: Enterprise Audit Event Architecture & Provenance Model

## Status
Accepted

## Context
Standard application logging (e.g. `logger.info(...)`) lacks institutional provenance, tenant boundary guarantees, cryptographic immutability, and contextual correlation. Enterprise customers and regulatory auditors (SOC 2, GDPR, HIPAA, EU AI Act) require complete evidence explaining what happened, who acted, why it happened, which AI models and datasets participated, and which policy decisions governed execution.

## Decision
We implemented a universal `AuditEvent` architecture under `app/audit/core/`:
1. **Universal Model**: Every audit record captures:
   - Tenant, Organization, Workspace, and Environment isolation boundaries.
   - Actor identification (`USER`, `AGENT`, `SYSTEM`, `SERVICE`, `API_CLIENT`, `ADMIN`, `AUTOMATION`).
   - Target Resource (`workflow`, `agent`, `model`, `prompt`, `document`, `policy`, `secret`, `database`).
   - Execution metrics: severity, outcome, risk score, duration, and status codes.
2. **Correlation Graph**: Propagates `request_id`, `correlation_id`, `parent_event_id`, `workflow_id`, and `agent_id` across asynchronous multi-agent workflows, enabling full execution timeline reconstruction.
3. **Cryptographic Binding**: Each event is bound to an immutable SHA-256 integrity hash and digital signature.

## Consequences
### Positive
- Unified institutional memory of all critical platform, AI, and workflow actions.
- Full provenance enabling retrospective audits and forensic investigation.
- Seamless correlation across asynchronous agent swarms and human workflows.

### Negative / Trade-offs
- Modest storage and compute overhead for event normalization and signature calculation.
