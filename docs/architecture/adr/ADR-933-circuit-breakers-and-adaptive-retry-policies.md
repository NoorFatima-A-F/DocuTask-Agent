# ADR-933: Circuit Breakers, Bulkhead Isolation & 5 Retry Strategies

## Status
Accepted

## Context
Cascading upstream failures, thundering herds on recovery, and resource saturation across unisolated workloads threaten whole-platform availability during third-party or internal outages.

## Decision
We introduce `ReliabilityPolicyEngine` supporting 3-state `CircuitBreaker` (`CLOSED`, `OPEN`, `HALF_OPEN`), `Bulkhead` concurrency and wait-queue limits, and 5 backoff strategies (`IMMEDIATE`, `LINEAR`, `EXPONENTIAL`, `RANDOMIZED_JITTER`, `ADAPTIVE`).

## Consequences
- Fast-failing calls when downstream services or AI providers are unavailable, preventing thread pool exhaustion.
- Jittered exponential and adaptive backoffs eliminate synchronous retry storms.
- Transparent fallbacks (e.g. cached responses or alternative models) maintain degraded functionality.
