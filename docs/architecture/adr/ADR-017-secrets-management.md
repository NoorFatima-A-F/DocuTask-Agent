# Architecture Decision Record: ADR-017

## Title
Enterprise Secrets Management: Tenant Partitioning, Cryptographic Rotation, and Environment Isolation

## Status
**ACCEPTED** (2026-03-24)

## Context
Raw calls to `os.getenv("SECRET_KEY")` or hardcoded tokens scattered across domain and worker logic represent severe compliance and security vulnerabilities (SOC 2, HIPAA, ISO 27001). Furthermore, multi-tenant connectors require distinct per-tenant API tokens with independent rotation and revocation lifecycles.

## Decision
We enforce the **ISecretManager** interface as the sole mechanism for accessing, rotating, and revoking sensitive secrets. Secrets are partitioned by tenant context (`{tenant_id}:{key}`), support automated expiration and versioning, and strictly prohibit direct raw `os.getenv()` access outside the infrastructure secrets layer.

## Consequences
### Positive
- Strict cryptographic isolation of third-party integration tokens per customer tenant.
- Seamless rotation and revocation without platform restarts.
- Compatible with cloud secret stores (AWS Secrets Manager, GCP Secret Manager, Vault).
### Negative / Trade-Offs
- Subsystems must inject `ISecretManager` to access integration credentials.
