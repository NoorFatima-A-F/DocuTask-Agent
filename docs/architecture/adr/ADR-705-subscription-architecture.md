# ADR-705: Subscription Architecture

## Status
Accepted

## Context
Commercial monetization requires supporting multi-tier SaaS packaging (Free, Developer, Professional, Business, Enterprise, Custom) without coupling feature code to hardcoded tier checks.

## Decision
1. Define formal `Subscription` entities with structured feature entitlements and quota limits.
2. Implement `FeatureEntitlementService` to decouple feature enablement from pricing plans.
3. Feature checks evaluate against dynamic catalog rules and per-tenant feature overrides.

## Consequences
- **Positive**: Clean separation between commercial packaging and runtime logic; flexible custom enterprise contracts.
- **Trade-off**: Requires synchronizing subscription state with external payment processors (e.g. Stripe).
