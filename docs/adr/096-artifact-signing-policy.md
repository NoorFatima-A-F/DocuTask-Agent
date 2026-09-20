# 96. Cryptographic Artifact Signing & Verification Policy

Date: 2026-09-20

## Status
Accepted

## Context
Deploying unauthenticated binaries risks supply chain compromise. Signing must support keyless OIDC identities, KMS-backed keys, and private keys.

## Decision
We implement `SigstoreCosignAdapter` and `SupplyChainPolicyEnforcer`.
Production policy mandates:
`Artifact Digest Valid AND Signature Valid AND Signer Trusted AND SBOM Present AND Provenance Present AND Security Scan Passed`.
Any missing requirement triggers `DEPLOYMENT DENIED`.

## Consequences
- Keyless signing enables short-lived, verifiable developer and CI identities.
- Cryptographic verification happens at control plane admission time prior to cluster rollout.
