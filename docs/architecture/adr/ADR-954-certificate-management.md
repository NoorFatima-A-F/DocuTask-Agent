# ADR-954: Automated Certificate Authority & X.509 Lifecycle Management

## Status
Accepted

## Context
Manual TLS certificate management leads to service outages from unexpected certificate expiration, unmanaged private keys, and slow incident response during cryptographic key compromises.

## Decision
We implement `CertificateAuthorityManager` supporting:
1. Hierarchical Root and Intermediate CAs.
2. Automated X.509 certificate issuance for all registered workloads with short default validity windows (30 days).
3. Zero-downtime certificate rotation without service restarts.
4. Real-time Certificate Revocation Lists (CRL) and trust bundle distribution to mesh sidecars.

## Consequences
- Total elimination of expired certificate outages through automated rotation.
- Rapid containment of compromised private keys via instant CRL revocation.
- Uniform trust chain established across multi-region and hybrid cloud clusters.
