# ADR-005: HMAC-SHA256 Cryptographic Certification Authority

## Status
Accepted

## Context
CI/CD release gates, deployment pipelines, and compliance auditors require proof that a verification run succeeded and was not modified post-run.

## Decision
We implemented a Cryptographic Certification Authority:
- Generates `ComplianceCertificate` upon successful quality gate pass.
- Computes canonical hash over `(run_id, suite_id, status, overall_score, timestamp)`.
- Signs the hash with HMAC-SHA256 using an isolated master secret.
- Provides constant-time verification `verify_certificate(cert)` for third-party validation.

## Consequences
### Positive
- Cryptographically verifiable release gating.
- Eliminates manual audit sign-off friction.

### Negative
- Requires secure key management for enterprise deployments.
