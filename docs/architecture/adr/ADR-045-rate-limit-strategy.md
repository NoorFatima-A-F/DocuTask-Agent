# ADR-045: Multi-Tenant Hierarchical Rate Limiting Strategy

## Status
Accepted

## Context
High-concurrency autonomous workflows and agents can rapidly exhaust third-party API rate quotas (e.g. 429 Too Many Requests), resulting in IP bans, tenant starvation, and service disruption across all workflows sharing that connector.

## Decision
We implement a multi-tiered `RateLimiter` supporting both Token Bucket and Sliding Window algorithms. Rate limits are evaluated hierarchically across:
1. `Organization` tier
2. `Workspace` tier
3. `Connector` tier
4. `Credential` tier
5. `User / Agent` tier

When capacity is exhausted, the engine calculates deterministic `retry_after_seconds` and raises a typed `RateLimitExceededError`.

## Consequences
- Prevents noisy-neighbor starvation across multi-tenant workloads.
- Avoids upstream vendor throttling by smoothing bursts.
- Provides precise backoff hints to the workflow scheduler and retry engine.
