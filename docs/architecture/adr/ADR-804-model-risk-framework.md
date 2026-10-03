# ADR-804: Quantitative Model Risk Assessment & Multi-Dimensional Scoring Framework

## Status
Accepted

## Context
Enterprise AI operations are subject to emerging compliance frameworks (EU AI Act, NIST AI RMF, ISO 42001). Qualitative risk descriptions are insufficient for automated policy evaluation.

## Decision
We implement `ModelRiskScorer` and `ModelRiskProfile` providing normalized quantitative evaluation across 4 dimensions:
1. `Security Risk`: Vulnerability to prompt extraction, adversarial attacks, and prompt injection.
2. `Compliance Risk`: Data retention policies, training data licensing, and geographic sovereignty.
3. `Robustness Risk`: Determinism, hallucination probability, and out-of-distribution stability.
4. `Fairness & Bias Risk`: Representation bias and toxic output probability.

The framework produces a composite weighted risk score mapped to discrete ratings (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), directly evaluated by the `ModelPolicyEnforcer`.

## Consequences
- **Positive**: Standardized risk quantification, automated risk-based policy blocking.
- **Negative**: Requires structured benchmark results and security assessments for all models.
