# Deep Health Probing & Anti-Flap Operational Guide

## 1. Six Probe Classifications
1. **STARTUP**: Verifies cold start initialization, environment hydration, and schema migration.
2. **READINESS**: Determines if component is ready to accept user traffic and execution requests.
3. **LIVENESS**: Verifies internal loops, process responsiveness, and thread deadlocks.
4. **DEPENDENCY**: Validates reachability and latency of downstream databases, cache, queues, and AI providers.
5. **RESOURCE**: Monitors memory thresholds, disk volume capacity, and GPU memory exhaustion.
6. **BUSINESS**: Evaluates workflow processing throughput, SLA margin trends, and business rule viability.

## 2. Flap Suppression Engine
The `FlapDetector` inspects state transitions over a rolling sliding window (default 60 seconds). When a component oscillates between `HEALTHY` and `UNHEALTHY` more than $N$ times ($N \ge 4$), the state is locked into `DEGRADED (FLAPPING)` to prevent failover loops until stability is re-established.
