# ADR-844: Controlled Human Override Governance & Audit Boundaries

## Status
Accepted

## Context
When AI systems make incorrect extraction or classification decisions, human operators must be able to intervene and correct the outcome. However, unrestricted manual overrides introduce security vulnerabilities, rogue modifications, and audit gaps.

## Decision
We implemented the Controlled Human Override Platform under `app/oversight/overrides/`:
1. **Safety Boundary Validation**: `OverrideValidator` enforces role permissions, minimum justification length, non-overrideable safety thresholds (e.g. risk score > 0.95), and strictly prohibited system actions.
2. **Immutable Intervention Ledger**: `OverrideService` persists `HumanOverrideRecord` containing original AI output, modified human value, justification, timestamp, and reviewer credentials.
3. **Feedback Loop Telemetry**: Manual overrides feed into `OversightMetricsCollector` to track AI error patterns and prompt/model drift.

## Consequences
### Positive
- Enforces strict justification and permission controls on human interventions.
- Full cryptographic traceability of all manual changes.
- Direct feedback telemetry for continuous AI model alignment.

### Negative / Trade-offs
- Requires administrative policy management for override permission boundaries.
