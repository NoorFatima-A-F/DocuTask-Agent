# Traffic Management & Resilience Operational Guide

## 1. Load Balancing Strategies
`LoadBalancerEngine` supports:
- `ROUND_ROBIN`: Sequential distribution across healthy endpoints.
- `LEAST_CONNECTIONS`: Dispatches to worker with fewest active concurrent streams.
- `LATENCY_BASED`: Routes to endpoint with lowest observed latency.
- `WEIGHTED`: Proportional distribution based on assigned endpoint weights.
- `GEO_AWARE`: Routes to instances in the local availability zone or region.

## 2. Canary Splits & Blue/Green Deployments
```python
from app.infrastructure.networking.traffic import TrafficRouter
from app.infrastructure.networking.control_plane import RouteRule, NetworkEndpoint

router = TrafficRouter()

# Blue/Green version toggle
router.set_blue_green_version("ingestion-service", active_version="green")
active = router.get_blue_green_version("ingestion-service")
```

## 3. Circuit Breaker & Outlier Ejection
```python
from app.infrastructure.networking.traffic import TrafficFailoverManager, CircuitBreakerConfig, CircuitState

cb_mgr = TrafficFailoverManager(CircuitBreakerConfig(
    consecutive_errors_threshold=5,
    recovery_time_seconds=30.0,
    half_open_success_threshold=3
))
```
