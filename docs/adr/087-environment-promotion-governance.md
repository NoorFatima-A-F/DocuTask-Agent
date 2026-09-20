# 87. Environment Promotion Governance & Validation

Date: 2026-09-19

## Status
Accepted

## Context
Deploying unverified changes directly to production creates reliability and compliance hazards. Clear promotion rules must govern the transition between environment tiers.

## Decision
We implement a `PromotionManager` backed by `PromotionPolicy` and `EnvironmentValidator`.
Releases must progress through `dev` -> `testing` -> `staging` -> `prod` with enforced soak time, test pass rate thresholds, and role-based approval gates (e.g. `release_manager`, `security_lead`).

## Consequences
- Bypassing lower environments is prevented.
- Complete audit trails record who requested, approved, and executed promotions.
