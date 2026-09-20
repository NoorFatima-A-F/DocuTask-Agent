# 85. Artifact Registry, Provenance & Cryptographic Signing

Date: 2026-09-19

## Status
Accepted

## Context
Enterprise security policies require full Software Bill of Materials (SBOM), vulnerability threshold enforcement, and tamper-proof verification for all build artifacts deployed to production.

## Decision
We implement an `ArtifactRegistry` that enforces SHA-256 content hashing, HMAC-SHA256 signature verification, and automated vulnerability scanning gates before artifacts are marked eligible for promotion.

## Consequences
- Unsigned or altered artifacts fail pre-flight validation and cannot be deployed.
- Complete dependency provenance is stored alongside build metadata.
