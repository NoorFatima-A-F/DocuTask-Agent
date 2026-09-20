# ADR-003: Bootstrap Confidence Intervals and Welch's Drift Detection

## Status
Accepted

## Context
LLM evaluations and OCR accuracy metrics exhibit non-normal, skewed, and heteroskedastic distributions. Traditional Gaussian assumptions ($Mean \pm 1.96 \times SD$) produce erroneous confidence boundaries.

## Decision
We implement:
1. **Non-parametric Bootstrap Resampling** (1,000 iterations) to compute 95% Confidence Intervals ($[CI_{2.5}, CI_{97.5}]$).
2. **Welch's Two-Sample t-Test** to compare current run distributions against golden baselines without assuming equal variances.
3. **Drift Detection**: Automatic flagging when $p < 0.05$ and the candidate mean degraded beyond allowed tolerance.

## Consequences
### Positive
- Mathematically rigorous evaluation regardless of sample distribution shape.
- Defensible auditing for regulatory scrutiny.

### Negative
- Minor CPU computation overhead for 1,000 bootstrap resamples (optimized via vectorized Python operations).
