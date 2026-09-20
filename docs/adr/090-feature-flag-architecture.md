# 90. Feature Flag Architecture & Safe Decoupled Rollouts

Date: 2026-09-19

## Status
Accepted

## Context
Deploying code to production should not automatically expose new features to 100% of tenants or users. Deployment (shipping bits) must be decoupled from release (enabling capabilities).

## Decision
We implement `FeatureFlagManager` and `FlagEvaluator`.
Flags support master toggles, tenant allowlisting, environment isolation, consistent SHA-256 hash-based percentage rollouts, and instant emergency kill-switches.

## Consequences
- Features can be tested in production by internal tenants before global exposure.
- Any faulty feature can be deactivated in sub-second time without redeploying code or initiating rollbacks.
