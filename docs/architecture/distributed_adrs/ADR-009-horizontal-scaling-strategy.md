# ADR-009: Horizontal Scaling & Amdahl's Law Bottleneck Modeling

**Status**: **ACCEPTED**  
**Date**: 2026-08-19  

## 1. Context & Problem Statement
Define horizontal scaling thresholds for worker nodes and model diminishing returns.

## 2. Decision Outcome
Set auto-scaling policy: scale out workers when queue depth > 50 or CPU > 70%. Model scaling limits using Amdahl's Law ($S_{latency}(s) = \frac{1}{(1-p) + \frac{p}{s}}$ where serial fraction $1-p \approx 5\%$).

## 3. Consequences
- **Positive**: Scaling efficiency remains $\ge 80\%$ up to 20 concurrent worker nodes.
