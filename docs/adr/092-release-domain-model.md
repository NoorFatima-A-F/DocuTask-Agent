# 92. Immutable Release Domain Model & Lifecycle

Date: 2026-09-20

## Status
Accepted

## Context
Rebuilding artifacts for each environment creates supply chain vulnerabilities and non-deterministic behavior. Releases must be immutable, versioned, and directly mapped to exact source commits.

## Decision
We define an immutable `Release` entity that binds source commit, build parameters, content-addressed artifact digests, SBOMs, SLSA provenance, and cryptographic signatures. Once published (`RELEASED`), a release version cannot be mutated.

## Consequences
- The exact same verified artifact is promoted across development, staging, and production tiers.
- Prevents drift caused by environment-specific rebuilds.
