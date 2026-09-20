# ADR-093: OCI 1.1 Artifact Referrers & Content-Addressed Storage

## Status
Accepted

## Context
Artifact integrity across container images, Helm charts, and configuration bundles requires strict cryptographic content addressing and standardized metadata association (SBOMs, signatures, attestations).

## Decision
1. All artifacts are stored content-addressed by SHA-256 / SHA-512 cryptographic digests.
2. We adopt the OCI 1.1 Referrers Specification (`OCIReferrerDescriptor`, `OCIManifest`) to link auxiliary artifacts (CycloneDX SBOMs, SLSA provenance statements, Cosign signature bundles) directly to target base image digests in the registry.

## Consequences
- Enables decentralized verification of supply-chain attestations without modifying base container layers.
