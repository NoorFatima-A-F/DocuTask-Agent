# ADR-092: Immutable Release Domain Model & SemVer Compatibility Matrix

## Status
Accepted

## Context
Deploying multi-component architectures (API gateways, worker pools, database schemas, and developer SDKs) often causes silent runtime failures due to mismatched major/minor API versions.

## Decision
1. All releases are modeled as immutable `Release` entities identified by a unique ID and canonical version.
2. Once registered, release manifests cannot be modified.
3. A centralized `ReleaseCompatibilityMatrix` evaluates semantic version constraints across API, SDK, worker nodes, and database schema revisions prior to authorizing deployment.

## Consequences
- Prevents cross-component version drift and invalid rollouts before any infrastructure resources are provisioned.
