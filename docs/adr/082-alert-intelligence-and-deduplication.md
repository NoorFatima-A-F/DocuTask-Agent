# ADR 082: Alert Intelligence, Deduplication & Storm Dampening

## Status
Accepted

## Context
High-volume microservice fleets generate noisy alert storms during cascading failures, causing alert fatigue and delayed incident triage.

## Decision
Deploy an intelligent Alert Management Engine (`AlertEngine`, `AlertRouter`):
1. Deduplicate repetitive alerts within a sliding window.
2. Rate-limit and group alerts by incident correlation keys.
3. Multi-channel routing based on severity thresholds (Slack, PagerDuty, Webhooks, Email).

## Consequences
- **Positive**: Eliminates alert fatigue, escalates high-priority signals immediately, groups correlated alarms.
- **Negative**: Rule thresholds must be tuned periodically to prevent false positives.
