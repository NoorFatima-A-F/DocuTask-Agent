# ADR-854: Multi-Category AI Risk Scoring & Trend Intelligence

## Status
Accepted

## Context
AI risk is multidimensional, encompassing security threats, privacy violations, regulatory non-compliance, foundation model hallucination/drift, prompt injection vulnerabilities, data misuse, operational downtime, and unexpected financial costs. Static thresholding fails to capture systemic, emerging patterns.

## Decision
We implemented a multi-category risk intelligence engine under `app/governance/analytics/risk/`:
1. **Multi-Factor Scoring Formula**: Evaluates $\text{Risk Score} = \text{Impact} \times \text{Probability} \times \text{Exposure} \times \text{Category Weight}$.
2. **Eight Core Taxonomies**: Evaluates Security, Privacy, Compliance, Model, Prompt, Data, Operational, and Financial risks.
3. **Automated Trend Detection**: `RiskTrendAnalyzer` continuously flags anomaly signals including `SUDDEN_RISK_SPIKE`, `REPEATED_VIOLATIONS`, `UNCONTROLLED_AGENT`, and `UNSAFE_MODEL`.

## Consequences
### Positive
- Actionable visibility into specific risk vectors rather than a single black-box score.
- Early warning detection for rogue agents or drifting models before catastrophic failures occur.
- Direct integration with platform alerting systems.

### Negative / Trade-offs
- Requires ongoing fine-tuning of category weights to reflect evolving regulatory standards.
