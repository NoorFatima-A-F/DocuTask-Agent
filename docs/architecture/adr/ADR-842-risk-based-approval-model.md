# ADR-842: Dynamic Risk-Based Approval & Multi-Level Workflow Model

## Status
Accepted

## Context
Fixed, static approval requirements either overburden human reviewers with trivial alerts (review fatigue) or fail to catch subtle, high-risk anomalies. Enterprise AI platforms require dynamic, context-aware policy evaluation that scales with risk, financial impact, data sensitivity, and extraction confidence.

## Decision
We implemented a dynamic risk-based policy and workflow engine under `app/oversight/approvals/` and `app/oversight/workflows/`:
1. **Dynamic Policy Conditions**: `ApprovalPolicyEngine` evaluates composite conditions against `OversightContext` attributes (risk score, confidence, financial value, data classification).
2. **Multi-Level Approval Strategies**:
   - `SEQUENTIAL`: Step-by-step tiered sign-offs (e.g. Operator -> Manager -> Compliance Officer).
   - `PARALLEL`: Concurrent sign-offs across multiple stakeholders.
   - `THRESHOLD`: $M$-of-$N$ consensus quorum across designated reviewer pools.
3. **Fail-Fast Safety**: Any rejection along an approval chain immediately halts execution and prevents unauthorized downstream processing.

## Consequences
### Positive
- Prevents reviewer fatigue by filtering low-risk, high-confidence autonomous executions.
- Enforces strict dual-control and multi-tier sign-offs for high-impact transactions.
- Flexible orchestration adaptable to enterprise governance requirements.

### Negative / Trade-offs
- Multi-step approval workflows require asynchronous coordination and persistent state tracking.
