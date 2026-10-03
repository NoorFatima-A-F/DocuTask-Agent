# ADR-035: Composite Confidence Scoring & Risk Verification Model

## Status
Accepted

## Context
Autonomous agents must not make high-stakes enterprise decisions (such as multi-thousand dollar disbursements or legally binding contract approvals) on low-confidence or ungrounded outputs. A holistic scoring model is required to combine validation results, evidence support, policy compliance, and financial impact.

## Decision
We implement `ConfidenceEngine` generating composite `ConfidenceReport`s:
1. `Verification Score` (35% weight): Passed deterministic validation rules.
2. `Evidence Score` (25% weight): Ratio of verified supporting citations/evidence.
3. `Policy Compliance` (25% weight): Strict compliance with enterprise policy sets.
4. `Model Confidence` (15% weight): Raw confidence emitted by foundational models.
5. `Risk Assessment`: Financial impact thresholds (e.g., transactions $\ge \$10,000$), security violations, or compliance deviations.

If composite confidence falls below threshold (e.g. $< 0.80$) or risk exceeds threshold (e.g. $\ge 0.40$), the engine marks `requires_human_review = True` and triggers `HumanEscalationEngine`.

## Consequences
- Transparent, mathematical basis for human escalation.
- Prevents ungrounded hallucinations from executing high-impact business actions.
