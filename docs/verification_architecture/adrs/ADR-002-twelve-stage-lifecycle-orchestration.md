# ADR-002: Twelve-Stage Deterministic Lifecycle Orchestration

## Status
Accepted

## Context
Complex multi-domain verification requires structured preparation, execution, measurement, sealing, and cleanup. Without a unified lifecycle, test runs suffer from inconsistent setup, missing datasets, unsealed evidence, and incomplete teardowns.

## Decision
We define a strict 12-stage sequential lifecycle orchestrator:
1. `PRE_FLIGHT_DISCOVERY`
2. `DATASET_ACQUISITION`
3. `ENVIRONMENT_PROVISIONING`
4. `INVARIANT_REGISTRATION`
5. `PROBABILISTIC_EXECUTION`
6. `METRIC_COMPUTATION`
7. `STATISTICAL_ANALYSIS`
8. `EVIDENCE_SEALING`
9. `QUALITY_GATE_EVALUATION`
10. `COMPLIANCE_CERTIFICATION`
11. `TELEMETRY_EXPORT`
12. `POST_FLIGHT_TEARDOWN`

## Consequences
### Positive
- Guaranteed execution ordering and deterministic reproducibility.
- Clear stage-level observability and error localization.

### Negative
- Strict lifecycle requires all plugins to adhere to standard state transitions.
