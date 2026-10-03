# ADR-967: Feature Flag & Dynamic Runtime Targeting Platform

## Status
Accepted

## Context
Decoupling code deployment from feature release allows developers to ship code continuously while safely toggling feature availability based on tenant, user, environment, and percentage criteria.

## Decision
We implement `FeatureRolloutManager` supporting:
1. `FeatureFlag` definitions with fine-grained `RolloutRule` targeting (environment, tenant, specific user list, percentage hashing).
2. Consistent, deterministic percentage bucketing using MD5 hashing of entity keys.
3. Global emergency kill switches enabling instant runtime deactivation without service restarts or redeployments.

## Consequences
- Zero-risk progressive rollout of new agent runtime models and UI features.
- Instant mitigation of unexpected feature bugs via emergency kill switches.
- Controlled beta testing with enterprise VIP tenants.
