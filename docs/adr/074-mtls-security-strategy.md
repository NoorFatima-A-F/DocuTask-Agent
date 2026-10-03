# ADR 074: Mutual TLS 1.3 Transport Security & Certificate Lifecycle

## Status
Accepted

## Context
Data-in-transit across multi-cloud clusters must be encrypted with cryptographic identity verification on both ends of every TCP/HTTP/gRPC connection.

## Decision
Enforce TLS 1.3 mutual authentication (`MTLSManager`) utilizing modern cipher suites (`TLS_AES_256_GCM_SHA384`, `TLS_CHACHA20_POLY1305_SHA256`). Workload certificates are minted as short-lived X.509 SVIDs with SPIFFE SANs, managed by a multi-backend CA (`CertificateManager`), and rotated automatically without service restarts.

## Consequences
- **Positive**: Eliminates man-in-the-middle attacks, ensures cryptographic workload provenance.
- **Negative**: Requires automatic certificate rotation to prevent downtime from expired certificates.
