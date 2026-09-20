# ADR-706: Billing Separation

## Status
Accepted

## Context
Coupling runtime workflow or agent execution directly to third-party billing APIs creates latency, brittle external dependencies, and execution failures if billing systems become unavailable.

## Decision
1. Decouple runtime execution from billing via asynchronous `UsageMeteringPlatform` event generation.
2. Ingest usage telemetry into isolated `BillingFoundation` managing invoices, credits, discounts, and payment records.
3. Support prepaid balance credits, post-paid monthly invoices, and automated usage charge aggregation.

## Consequences
- **Positive**: Zero latency overhead on workflow execution; runtime remains resilient during billing gateway downtime.
- **Trade-off**: Requires periodic background reconciliation between metered usage and issued invoices.
