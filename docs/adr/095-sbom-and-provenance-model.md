# ADR-095: Software Bill of Materials (SBOM) & SLSA Level 3 Provenance

## Status
Accepted

## Context
Regulatory compliance and vulnerability response require exact dependency visibility and verifiable build environment attestation.

## Decision
1. The build pipeline automatically generates SBOMs in both CycloneDX 1.5 and SPDX 2.3 formats (`SBOMManager`).
2. Build provenance is formatted in accordance with the SLSA v1.0 specification within in-toto statement envelopes (`ProvenanceManager`).
3. `SBOMPolicyEvaluator` enforces license compliance (blocking viral copyleft such as AGPL-3.0 and GPL-3.0).

## Consequences
- Full automated compliance tracking and rapid zero-day vulnerability identification.
