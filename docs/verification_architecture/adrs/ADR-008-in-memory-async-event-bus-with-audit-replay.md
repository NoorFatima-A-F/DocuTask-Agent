# ADR-008: Asynchronous Event Bus with Audit Replay Capability

## Status
Accepted

## Context
Real-time UI streaming, telemetry logging, and forensic audit playback require decoupled event distribution during verification lifecycles.

## Decision
We implemented an Asynchronous Event Bus:
- Emits typed `VerificationEvent` objects (`STAGE_STARTED`, `INVARIANT_EVALUATED`, `EVIDENCE_STORED`, etc.).
- Handlers subscribe via asynchronous queues/callbacks.
- `TelemetrySink` records every event in an immutable event ledger, supporting filtered retrieval and audit replay.

## Consequences
### Positive
- Low latency, non-blocking telemetry and SSE streaming.
- Complete audit trail of every lifecycle step.

### Negative
- Memory retention of event history (governed by buffer limits in production).
