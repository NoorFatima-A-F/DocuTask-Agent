# ADR-824: Composite Multi-Factor AI Risk Scoring Framework

## Status
Accepted

## Context
AI risk is rarely single-dimensional. Evaluating risk solely on input keywords ignores the underlying model tier (Phase 8C), prompt volatility (Phase 8D), data sensitivity (Phase 8B), and tool capability. A holistic, weighted risk framework is necessary for granular decision-making.

## Decision
We implemented a composite multi-factor risk scoring engine (`CompositeRiskScorer`):
$$R_{\text{composite}} = w_{\text{in}}R_{\text{in}} + w_{\text{model}}R_{\text{model}} + w_{\text{prompt}}R_{\text{prompt}} + w_{\text{data}}R_{\text{data}} + w_{\text{tool}}R_{\text{tool}} + w_{\text{output}}R_{\text{output}}$$
1. **Input Risk ($R_{\text{in}}$)**: Intent classification, prompt injection confidence, jailbreak probability adjusted by source trust tier.
2. **Model Risk ($R_{\text{model}}$)**: Model risk tier from Phase 8C Model Registry (`CRITICAL`: 0.95, `HIGH`: 0.75, `MEDIUM`: 0.40, `LOW`: 0.10).
3. **Prompt Risk ($R_{\text{prompt}}$)**: Prompt complexity and variable exposure from Phase 8D.
4. **Data Sensitivity ($R_{\text{data}}$)**: Data classification from Phase 8B Data Governance (`RESTRICTED`: 0.90, `CONFIDENTIAL`: 0.60, `INTERNAL`: 0.30, `PUBLIC`: 0.05) + PII presence penalty.
5. **Tool Danger ($R_{\text{tool}}$)**: Max tool danger score in current context.
6. **Output Risk ($R_{\text{output}}$)**: Toxicity score, secret leakage indicators, and grounding failure margin.

## Consequences
### Positive
- Normalized $0.0 - 1.0$ risk score providing explainable, multi-dimensional risk visibility.
- Dynamic adaptation based on tenant and asset classification.
