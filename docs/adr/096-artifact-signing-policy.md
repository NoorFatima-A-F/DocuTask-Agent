# ADR-096: Cryptographic Artifact Signing with Sigstore, Cosign & Rekor

## Status
Accepted

## Context
Long-lived private signing keys are susceptible to compromise and management overhead.

## Decision
We adopt the Sigstore / Cosign ecosystem (`SigstoreCosignAdapter`):
1. Keyless signing using OpenID Connect (OIDC) identities.
2. Signatures and certificate bundles are logged to the public Rekor transparency log.
3. Verification is integrated into the pre-deployment admission controller.

## Consequences
- Eliminates key management friction while providing tamper-evident public audit logs.
