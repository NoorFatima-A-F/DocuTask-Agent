# Multi-Environment Promotion & Isolation Guide

## 1. Environment Promotion Pipeline
`Development (Dev)` -> `Testing / QA (Test)` -> `Staging` -> `Production (Prod)` -> `Customer Managed / Air-Gapped`.

## 2. Environment Promotion Gating
| Environment | Approval Required | Min Test Coverage | Vulnerability Policy | Artifact Signing |
|---|---|---|---|---|
| **Dev** | 0 | 0% | Warn only | Optional |
| **Test** | 0 | 80% | Block Critical | Required |
| **Staging** | 1 (Lead Dev) | 80% | Block Critical | Required |
| **Prod** | 2 (Lead + Sec) | 85% | Block Critical & High | Required |

```python
from app.infrastructure.deployment.environments import EnvironmentPromotionManager

promo_mgr = EnvironmentPromotionManager()
checklist = promo_mgr.evaluate_promotion(
    from_env="staging",
    to_env="prod",
    release_id="rel-200",
    artifact=artifact,
    tests_passed=True,
    approvers=["lead-dev", "security-officer"],
)
assert checklist.is_eligible is True
```
