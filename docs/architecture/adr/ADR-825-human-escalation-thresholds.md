# ADR-825: Action Thresholds and Human Escalation Governance

## Status
Accepted

## Context
Automated safety systems must balance protection with operational continuity. Hard-blocking every borderline request causes developer friction, while fully autonomous execution on destructive tools risks catastrophic errors. Clear, graduated action thresholds are required.

## Decision
We established a 4-tier risk threshold policy mapped directly to gateway enforcement statuses:
1. **Low Risk ($R_{\text{composite}} < 0.30$) $\to$ `ALLOW`**: Normal automated execution without interruption.
2. **Medium Risk ($0.30 \le R_{\text{composite}} < 0.60$) $\to$ `ALLOW_WITH_AUDIT` / `MODIFY`**: Automated execution with mandatory audit logging and optional PII auto-redaction.
3. **High Risk ($0.60 \le R_{\text{composite}} < 0.85$) $\to$ `REQUIRE_HUMAN` / `ESCALATE`**: Operation is paused and assigned to a designated human supervisor in the review queue.
4. **Critical Risk ($R_{\text{composite}} \ge 0.85$ or Critical Violation) $\to$ `BLOCK`**: Immediate termination, refusal generation, and automatic `SafetyIncident` lifecycle creation.

## Consequences
### Positive
- Predictable and auditable risk response matrix.
- Guarantees high-risk operations undergo human sign-off without choking low-risk operational throughput.
