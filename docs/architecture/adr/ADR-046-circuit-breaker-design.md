# ADR-046: Four-State Circuit Breaker Resilience Design

## Status
Accepted

## Context
When an external SaaS provider experiences a major outage or prolonged latency spikes, continued invocations by pending workflows tie up thread pools, consume memory, and cause cascading system failures across the DocuTask Agent kernel.

## Decision
We implement a four-state `CircuitBreaker` (`CLOSED`, `OPEN`, `HALF_OPEN`, `RECOVERY`) attached to every connector endpoint:
- `CLOSED`: Normal traffic. Failures are tracked over a sliding window.
- `OPEN`: Tripped upon exceeding consecutive failure threshold (default 5). Calls fail immediately with `CircuitBreakerOpenError` without hitting the network.
- `HALF_OPEN`: Entered after `recovery_timeout_seconds` (default 10s). Allows limited probe requests.
- `RECOVERY`: Progressive verification before full restoration to `CLOSED`.

## Consequences
- Fast-fails requests during third-party outages, preventing resource exhaustion.
- Protects external services from thundering herds during recovery.
- Enables workflow engine to execute fallback saga branches immediately.
