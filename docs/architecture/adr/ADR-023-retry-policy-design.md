# Architecture Decision Record: ADR-023

## Title
Automated Retry Policies: Backoff Algorithms, Jitter, and Error Classification

## Status
**ACCEPTED** (2026-03-24)

## Context
Transient network glitches, API rate limits (HTTP 429), and temporary connector outages should not fail long-running workflows. Conversely, retrying non-transient deterministic errors (e.g., validation failures, unauthorized permissions) wastes compute resources and floods external APIs.

## Decision
We implement an **Intelligent RetryEngine**:
1. Support for `fixed`, `linear`, and `exponential` backoff strategies with full randomization jitter to prevent thundering herd spikes.
2. Strict error classification: Transient network/timeout errors are retried up to configured budgets; deterministic business validation and security exceptions immediately terminate without retry.

## Consequences
### Positive
- Autonomous self-healing for transient failures.
- Zero wasted retries on deterministic failures.
### Negative / Trade-Offs
- Tasks must be idempotent to prevent duplicate side effects during retries.
