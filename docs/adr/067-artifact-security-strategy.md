# ADR-067 / ADR-964: Software Supply Chain Security & Artifact Cryptographic Signing

## Status
Accepted

## Context
Supply chain vulnerabilities (tampered container layers, malicious upstream dependencies, compromised build systems) threaten the integrity of enterprise AI deployments.

## Decision
We implement `ArtifactRegistry` and `ArtifactSigner` adhering to modern SLSA/Cosign principles:
1. Every container image, wheel, and model bundle is indexed with an SBOM and immutable SHA-256 digest.
2. Cryptographic signature generation and verification on all promotion steps.
3. Vulnerability scanning with hard policy blocks on CRITICAL and HIGH severity CVEs for production promotion.

## Consequences
- Guaranteed artifact immutability and provenance tracking from source build to production cluster.
- Automated blocking of untrusted, tampered, or vulnerable dependencies.
- Enterprise compliance readiness for SOC2, FedRAMP, and ISO 27001 supply chain audits.
