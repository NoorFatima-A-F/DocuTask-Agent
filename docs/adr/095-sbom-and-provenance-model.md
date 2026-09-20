# 95. SBOM & Provenance Attestation Model

Date: 2026-09-20

## Status
Accepted

## Context
Compliance frameworks (SOC 2, ISO 27001, Executive Order 14028) require verifiable bills of materials and build provenance.

## Decision
We implement `SBOMManager` (generating CycloneDX 1.5 and SPDX 2.3 documents) and `ProvenanceManager` (generating SLSA v1.0 / in-toto statements). Attestations are linked directly to artifact digests and verified during promotion gates.

## Consequences
- Banned licenses (e.g. AGPL/GPL) and known CVEs are automatically detected and blocked.
- Build parameters, compiler versions, and material hashes are recorded immutably.
