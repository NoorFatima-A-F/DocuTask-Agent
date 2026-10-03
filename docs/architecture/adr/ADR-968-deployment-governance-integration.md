# ADR-968: Deployment Governance & Multi-Pillar Platform Integration

## Status
Accepted

## Context
Deployments cannot operate in isolation from platform governance (Phase 8), high availability & incident state (Phase 9D), observability (Phase 9E), and zero-trust networking (Phase 9F).

## Decision
We integrate deployment control into the platform governance and reliability fabric:
1. Pre-flight verification blocks deployments during active critical incidents (Phase 9D) or when error budgets are exhausted (Phase 9E).
2. Deployment actions emit full telemetry traces, flow logs, and audit records into the centralized observability pipeline.
3. Newly deployed services automatically register with the service discovery catalog and receive mTLS identities (Phase 9F).

## Consequences
- Guaranteed platform stability by halting non-emergency deployments during outages.
- Unified governance compliance across all software and infrastructure changes.
- Automated end-to-end telemetry correlating code releases with downstream system performance.
