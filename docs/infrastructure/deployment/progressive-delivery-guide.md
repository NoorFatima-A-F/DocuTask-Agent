# Progressive Delivery & Deployment Strategies Guide

## 1. Supported Deployment Strategies
- **Rolling Deployment**: Replaces instances in configurable batches (e.g. 2 at a time) with health validation between batches.
- **Canary Deployment**: Shifts traffic progressively (1% -> 5% -> 25% -> 50% -> 100%) with automated error rate telemetry evaluation.
- **Blue-Green Deployment**: Deploys a full parallel green environment, runs comprehensive health probes, and performs an atomic DNS/Router cutover.
- **Shadow Deployment**: Mirrors live production traffic to a shadow version to evaluate AI inference output and latency without client impact.

## 2. Canary Rollout Configuration
```python
from app.infrastructure.deployment.strategies import CanaryDeploymentStrategy, CanaryStep

strategy = CanaryDeploymentStrategy(
    steps=[CanaryStep(1.0), CanaryStep(5.0), CanaryStep(25.0), CanaryStep(50.0), CanaryStep(100.0)],
    max_error_rate=0.01  # 1% error rate threshold triggers immediate rollback
)
```
