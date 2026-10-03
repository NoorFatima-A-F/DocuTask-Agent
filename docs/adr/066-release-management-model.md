# ADR-066 / ADR-963: Release Management Lifecycle & Multi-Role Approval Gates

## Status
Accepted

## Context
Deploying software updates without formalized release tracking and multi-stakeholder governance risks releasing untested changes or unreviewed security modifications into production environments.

## Decision
We implement `ReleaseManager` enforcing a 7-stage release lifecycle:
`CREATED` -> `VALIDATED` -> `APPROVED` -> `RELEASED` -> `DEPLOYED` -> `MONITORED` -> `COMPLETED`.
Advancement to `RELEASED` mandates sign-offs across mandatory stakeholder roles (`governance`, `security`, `sre`) via `ReleaseApprovalGate`.

## Consequences
- Formal release gating prevents rogue or unvetted releases from entering production.
- Full traceability linking release versions to specific artifact digests and git commits.
- Semantic Versioning (SemVer 2.0.0) validation on all release creations.
