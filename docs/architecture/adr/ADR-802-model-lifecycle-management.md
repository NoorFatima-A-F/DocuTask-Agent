# ADR-802: 9-State Model Lifecycle State Machine & Multi-Stage Approval Workflow

## Status
Accepted

## Context
Deploying enterprise AI models without strict gatekeeping risks deploying models that breach privacy policies, exceed cost budgets, or fail security audits.

## Decision
We enforce a deterministic 9-state finite state machine (FSM):
`REGISTERED` -> `EVALUATING` -> `REVIEW` -> `APPROVED` -> `ACTIVE` -> `RESTRICTED` -> `DEPRECATED` -> `RETIRED` -> `ARCHIVED`.

Transition into `APPROVED` and `ACTIVE` requires successful progression through a 5-stage approval workflow:
1. `TECHNICAL_VALIDATION`: Capability and latency benchmarking.
2. `SECURITY_REVIEW`: Prompt injection and jailbreak robustness analysis.
3. `COMPLIANCE_AUDIT`: Data residency and GDPR/EU AI Act conformity.
4. `BUSINESS_APPROVAL`: Budget and commercial licensing sign-off.
5. `FINAL_GATE`: Enterprise sign-off before production activation.

## Consequences
- **Positive**: Strict regulatory compliance, tamper-proof state transitions, comprehensive audit trail of every model change.
- **Negative**: Adds formal gatekeeping review steps before model promotion.
